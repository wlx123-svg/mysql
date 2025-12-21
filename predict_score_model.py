import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

# ===================== 核心修正1：读取正确的文件名称 =====================
csv_file_path = 'student_data_adjusted_rounded.csv'

try:
    score_df = pd.read_csv(csv_file_path)
except FileNotFoundError:
    print(f"错误：未找到文件 {csv_file_path}，请确认文件路径和名称是否正确！")
    print("请确保该文件与 save_score_model.py 放在同一目录下")
    exit(1)

# 删除缺失值
score_df.dropna(inplace=True)

# 打印CSV的所有列名，方便核对
print("CSV文件中的所有列名：")
print(score_df.columns.tolist())

# ===================== 核心修正2：使用与CSV匹配的真实列名 =====================
feature_cols = [
    '每周学习时长（小时）',
    '上课出勤率',
    '作业完成率',
    '期中考试分数'
]
target_col = '期末考试分数'

# 校验列名是否存在
missing_cols = [col for col in feature_cols + [target_col] if col not in score_df.columns]
if missing_cols:
    print(f"错误：CSV文件中缺少以下列名：{missing_cols}")
    print("请核对CSV列名后修改 feature_cols/target_col！")
    exit(1)

# 定义特征和目标变量
features = score_df[feature_cols]
output = score_df[target_col]

# 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(
    features, output, train_size=0.8, random_state=42
)

# 构建并训练随机森林回归模型
rfr = RandomForestRegressor(n_estimators=100, random_state=42)
rfr.fit(x_train, y_train)

# 评估模型
y_pred = rfr.predict(x_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
print(f'模型均方根误差(RMSE): {rmse:.2f}')
print(f'模型预测分数范围: {y_pred.min():.1f} - {y_pred.max():.1f}')

# 保存模型
with open('score_model.pkl', 'wb') as f:
    pickle.dump(rfr, f)

print('成绩预测模型保存成功！生成文件：score_model.pkl')


def predict_score(input_features):
    """
    预测成绩函数
    :param input_features: 包含特征的字典，键为feature_cols中的列名
    :return: 预测的成绩
    """
    # 加载模型
    try:
        with open('score_model.pkl', 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        print("错误：未找到模型文件 score_model.pkl，请先训练模型！")
        return None
    
    # 转换输入为模型需要的格式
    input_df = pd.DataFrame([input_features])
    
    # 检查输入特征是否完整
    missing_features = [col for col in feature_cols if col not in input_df.columns]
    if missing_features:
        print(f"错误：缺少必要的特征：{missing_features}")
        return None
    
    # 进行预测
    prediction = model.predict(input_df)
    return round(prediction[0], 1)

    
    # 进行预测
    predicted_score = predict_score(sample_input)
    if predicted_score is not None:
        print(f"\n预测的期末考试分数为：{predicted_score}")
