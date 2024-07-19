import torch
from transformers import BertTokenizer, BertModel
from .models import embeddings, db
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


# 使用 BERT 分词器和模型生成嵌入向量。
def text_to_embedding(text):
    tokenizer = BertTokenizer.from_pretrained('D:\code\demo\\flaskr\\rag\\bert\huggingface\\bert-base-uncased')
    model = BertModel.from_pretrained('D:\code\demo\\flaskr\\rag\\bert\huggingface\\bert-base-uncased')
    encode_input = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**encode_input)
        embedding = outputs.last_hidden_state.mean(dim=1).numpy().astype(np.float32)
    return embedding

















#用于获取BERT模型的词嵌入
def bert_embedding(text):
    if text == '':
        return None
    # 初始化 BERT 的 tokenizer 和 model，使用预训练的 'bert-base-uncased' 模型
    # tokernizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokernizer = BertTokenizer.from_pretrained('D:\code\demo\\flaskr\\rag\\bert\huggingface\\bert-base-uncased')
    model = BertModel.from_pretrained('D:\code\demo\\flaskr\\rag\\bert\huggingface\\bert-base-uncased')

    # 使用 tokenizer 对输入文本进行编码，添加特殊 token 并将结果转换为 PyTorch 张量
    encode_input = tokernizer.encode_plus(
        text, # 输入的文本
        add_special_tokens=True, # 添加特殊的开始和结束 token
        return_tensors='pt'  # 返回 PyTorch 的张量
    )
    
    # 使用 torch.no_grad() 上下文管理器，禁用梯度计算，以提高推理速度并减少内存消耗
    with torch.no_grad():
        # 将编码后的输入传递给 BERT 模型，获取模型的输出
        outputs = model(**encode_input)
        # 获取最后一层隐藏状态，这是 BERT 产生的词嵌入
        # squeeze(0) 用于移除维度为1的维度，使输出更符合预期的形状
        embeddingss = outputs.last_hidden_state.squeeze(0)
        # last_hidden_states = outputs.last_hidden_state
    for i, token_embedding in enumerate(embeddingss):
        # 创建一个 Embedding 对象，并设置其属性
        embedding_obj = embeddings()
        embedding_obj.embedding =' '.join(map(str, token_embedding.numpy()))
        # 将 Embedding 对象添加到数据库中
        db.session.add(embedding_obj)
        db.session.commit()

    return embeddingss




# 计算嵌入之间的余弦相似度
def get_most_similar_embedding(question_embedding):
    # 将 question_embedding 转换为二维数组，如果它还不是
    if question_embedding.ndim == 1:
        question_embedding = question_embedding[np.newaxis, :]

    db_embeddings = db.session.query(embeddings).all()
    max_similarity = -1
    most_similar_embedding = None

    for embedding_row in db_embeddings:
        # 从 Row 对象中获取字符串嵌入向量
        embedding_str = str(embedding_row.embedding)  # 确保是字符串类型

        # 将字符串嵌入向量转换为 NumPy 数组
        embedding_vector = np.fromstring(embedding_str, sep=' ', dtype=np.float32)
        embedding_vector = embedding_vector.reshape(1, -1)  # 确保它是二维数组

        # 计算余弦相似度
        similarity = cosine_similarity(question_embedding, embedding_vector)
        if similarity[0][0] > max_similarity:
            max_similarity = similarity[0][0]
            # 存储最相似的嵌入向量的 ID，用于返回
            most_similar_embedding_id = embedding_row.id

    # 使用最相似的嵌入向量的 ID 来获取相关的答案或数据
    # 例如，如果你的数据库中有一个相关的答案字段，你可以这样做：
    # most_similar_answer = db.session.query(Embedding).get(most_similar_embedding_id).answer

    return most_similar_embedding_id  # 或返回相关的答案
# 文本相似性检测：

# 计算不同文本之间的嵌入向量的相似度，以判断它们的相似性。
# 文本分类：

# 使用嵌入向量训练分类器，对文本进行分类。
# 情感分析：

# 分析文本的情感倾向，判断是正面、负面还是中性。
# 命名实体识别：

# 识别文本中的特定实体，如人名、地点、组织等。
# 问答系统：

# 理解问题并从文本中提取答案。
# 机器翻译：

# 将一种语言的文本翻译成另一种语言。
# 文本生成：

# 利用文本的嵌入向量生成新的文本内容。
# 文档聚类：

# 将内容相似的文档聚集在一起。
# 推荐系统：

# 根据用户的阅读习惯推荐相关文本。
# 信息检索：

# 改进搜索引擎，返回与查询最相关的结果。










