# save_model.py（修正版本）
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pickle

# 设置输出右对齐，防止中文不对齐
pd.set_option('display.unicode.east_asian_width', True)

# 读取数据集，并将字符编码指定为gbk，防止中文报错
insurance_df = pd.read_csv('insurance-chinese.csv', encoding='gbk')

# 将医疗费用定义为目标输出变量
output = insurance_df['医疗费用']

# 使用年龄、性别、BMI、子女数量、是否吸烟、区域作为特征列
features = insurance_df[['年龄','性别','BMI','子女数量','是否吸烟','区域']]

# 对特征列进行独热编码 - 与streamlit_predict.py保持一致
# 性别编码
features['性别'] = features['性别'].map({'女': 0, '男': 1})

# 吸烟编码
features['是否吸烟'] = features['是否吸烟'].map({'否': 0, '是': 1})

# 区域编码（独热编码）
region_dummies = pd.get_dummies(features['区域'], prefix='区域')
features = pd.concat([features.drop('区域', axis=1), region_dummies], axis=1)

# 添加性别独热编码列
features['性别_女'] = 1 - features['性别']
features['性别_男'] = features['性别']
features = features.drop('性别', axis=1)

# 添加吸烟独热编码列
features['是否吸烟_否'] = 1 - features['是否吸烟']
features['是否吸烟_是'] = features['是否吸烟']
features = features.drop('是否吸烟', axis=1)

# 打印特征信息
print("特征列名:", features.columns.tolist())
print("特征数量:", len(features.columns))

# 划分数据集
x_train, x_test, y_train, y_test = train_test_split(features, output, train_size=0.8, random_state=42)

# 构建随机森林回归模型
rfr = RandomForestRegressor(random_state=42)

# 训练模型
rfr.fit(x_train, y_train)

# 预测
y_pred = rfr.predict(x_test)

# 计算R²分数
r2 = r2_score(y_test, y_pred)

print(f'模型在测试集上的R²分数为: {r2:.4f}')
print(f'特征重要性: {rfr.feature_importances_}')

# 保存模型
with open('rfr_model.pkl', 'wb') as f:
    pickle.dump(rfr, f)

print('保存成功，已生成 rfr_model.pkl 文件。')
