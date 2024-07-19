import torch
from transformers import BertTokenizer, BertModel
from .models import embeddings, db

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










