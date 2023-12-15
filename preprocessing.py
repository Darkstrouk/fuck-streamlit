import os
import pandas as pd


# распаковываем датасеты 
folder_path = r'/Users/darkstrouk/Documents/МОВС Магистратура/Прикладной Python/hw_1/stepik_linear_models/datasets'

cnt = 1
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        file_name_without_extension = os.path.splitext(file_name)[0]
        globals()[f'df_{file_name_without_extension}'] = pd.read_csv(file_path)
        cnt += 1


# чистим данные
df_list = [df_D_clients, df_D_job, df_D_last_credit, df_D_loan, df_D_salary, df_D_target, df_D_work, df_D_close_loan, df_D_pens]

for df in df_list:
    #удаляем пропуски
    for index, row in df.iterrows():
        df.loc[index] = row.dropna()
    #удаляем дубли чисто по айди
    for column in df.columns:
        if column.startswith('ID'):  
            df.drop_duplicates(subset=column, inplace=True)
    #удаляем аномалии
    numeric_columns = df.select_dtypes(include=['int', 'float'])
    # numeric_columns = numeric_columns.loc[:, ~numeric_columns.columns.str.startswith(('ID', 'FLAG'))]
    for column in numeric_columns:
        mean = df[column].mean()
        std = df[column].std()
        lower_limit = mean - 3 * std
        upper_limit = mean + 3 * std
        df[column] = np.where((df[column] < lower_limit) | (df[column] > upper_limit), np.nan, df[column])


# склеиваем данные
df = df_D_clients.merge(df_D_job, left_on='ID', right_on='ID_CLIENT', how='left')
df = df.merge(df_D_last_credit, on='ID_CLIENT', how='left')
df = df.merge(df_D_loan, on='ID_CLIENT', how='left')
df = df.merge(df_D_salary, on='ID_CLIENT', how='left')
df = df.merge(df_D_target, on='ID_CLIENT', how='left')
df = df.merge(df_D_work, left_on='SOCSTATUS_WORK_FL', right_on='ID', how='left')
df = df.merge(df_D_close_loan, left_on='ID_LOAN', right_on='ID_LOAN', how='left')
df = df.merge(df_D_pens, left_on='SOCSTATUS_PENS_FL', right_on='ID', how='left')


# заполняем пропуски средним значением
for column in numeric_columns:
    if numeric_columns[column].isnull().sum() > 0:  
        mean_value = numeric_columns[column].mean()  
        numeric_columns[column].fillna(mean_value, inplace=True) 


# удаляем ненужные колонки
df.drop(['ID_CLIENT', 'ID_LOAN', 'ID_y', 'FLAG_x', 'ID', 'FLAG_y', 'ID_x'], axis=1, inplace=True)