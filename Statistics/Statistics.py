from Instruments.Config import DB
import pandas as pd
import matplotlib.pyplot as plt


async def get_data(start_date, end_date):
    async with DB() as conn:
        return await conn.fetch('''SELECT question_id, number, category, city, clicks, operator_calls
            FROM statistics WHERE date>= $1 AND date <= $2''', start_date, end_date)


async def excel_report(start, end):
    data = await get_data(start, end)
    df = await prepare_dataframe(data)
    await generate_diagrams(df)

    with pd.ExcelWriter('Statistics/Статистика.xlsx', engine='xlsxwriter') as writer:
        workbook = writer.book
        category_format = await create_category_format(workbook)

        await generate_sheet(writer, df, 'Все города', category_format)

        for city in df['Город'].unique():
            city_data = df[df['Город'] == city]
            await  generate_sheet(writer, city_data, city, category_format)


async def prepare_dataframe(data):
    df = pd.DataFrame(data, columns=['question_id', 'number', 'category', 'city', 'clicks', 'operator_calls'])
    df.rename(columns={
        'number': 'Номер',
        'city': 'Город',
        'clicks': 'Число кликов',
        'operator_calls': 'Вызовы оператора'
    }, inplace=True)
    return df


async def create_category_format(workbook):
    return workbook.add_format({
        'font_size': 12,
        'align': 'center',
        'valign': 'vcenter',
        'font_color': 'white',
        'bg_color': '#0100FA'})


async def generate_sheet(writer, data, sheet_name, category_format):
    report_rows = []

    for category in data['category'].unique():
        report_rows.append({'Номер': '', 'Город': category, 'Число кликов': '', 'Вызовы оператора': ''})
        for _, row in data[data['category'] == category].iterrows():
            report_rows.append({
                'Номер': row['Номер'], 'Город': row['Город'],
                'Число кликов': row['Число кликов'], 'Вызовы оператора': row['Вызовы оператора']})

    report_df = pd.DataFrame(report_rows)
    report_df.to_excel(writer, sheet_name=sheet_name, index=False)

    worksheet = writer.sheets[sheet_name]

    worksheet.set_column('B:B', 16)
    worksheet.set_column('C:C', 13)
    worksheet.set_column('D:D', 18)

    for row_num, row in enumerate(report_df.itertuples(), start=1):
        if row.Номер == '':
            worksheet.merge_range(row_num, 0, row_num, 3, row.Город, category_format)

    if sheet_name == 'Все города':
        worksheet.insert_image('F1', 'Statistics/Все города.png')
    elif sheet_name in data['Город'].unique():
        worksheet.insert_image('F1', f'Statistics/{sheet_name}.png')


async def generate_diagrams(df):
    plt.figure(figsize=(6, 3), dpi=500)
    plt.subplots_adjust(left=-0.25)
    category_summary_all = df.groupby('category')['Число кликов'].sum()

    wedges, texts, autotexts = plt.pie(
        category_summary_all,
        autopct=lambda p: f'{int(round(p * sum(category_summary_all) / 100))}',
        startangle=90)

    plt.legend(
        wedges,
        category_summary_all.index,
        loc="center left",
        bbox_to_anchor=(1, 0.5))

    plt.title('Статистика: все города', fontsize=16)
    plt.savefig('Statistics/Все города.png')
    plt.close()

    cities = df['Город'].unique()

    for city in cities:
        plt.figure(figsize=(6, 3), dpi=500)
        plt.subplots_adjust(left=-0.25)

        city_data = df[df['Город'] == city]
        category_summary_city = city_data.groupby('category')['Число кликов'].sum()

        wedges, texts, autotexts = plt.pie(
            category_summary_city,
            autopct=lambda p: f'{int(round(p * sum(category_summary_city) / 100))}',
            startangle=90)

        plt.legend(
            wedges,
            category_summary_city.index,
            loc="center left",
            bbox_to_anchor=(1, 0.5))

        plt.title(f'Статистика: {city}', fontsize=16)
        plt.savefig(f'Statistics/{city}.png')
        plt.close()
