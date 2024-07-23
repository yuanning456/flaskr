

from pathlib import Path
from flask import current_app
from openai import OpenAI
import requests
from .models import FileInfo, db, QnA
import os
from .bert import bert_embedding, text_to_embedding, get_most_similar_embedding, chunk_text
from .moonshot import chat
#文件上传 api POST https://api.moonshot.cn/v1/files

def get_client(url: str):
    client = OpenAI(
    api_key = "{os.getenv('MOONSHOT_SECRET_KEY')}",
    base_url = url,
)
    return client
def file_to_moonshot(filepath):
    client = OpenAI(
    api_key = "{os.getenv('MOONSHOT_SECRET_KEY')}",
    base_url = "https://api.moonshot.cn/v1",
)
    file_object = client.files.create(file=Path(filepath), purpose="file-extract")
    try:
        current_app.logger.error(file_object.json())
        id = file_object.id
        new_file = FileInfo(moonshot_id=id)
        db.session.add(new_file)
        db.session.commit()

    except UnicodeDecodeError as e:
        current_app.logger.error("Error decoding message: %s", str(e))
   
  
    return file_object


def file_list():
    headers = {
    "Authorization": f"Bearer {os.getenv('MOONSHOT_SECRET_KEY')}",
    "Content-Type": "application/json"
    }
    response = requests.get('https://api.moonshot.cn/v1/files', headers=headers)
    if response.status_code == 200:
        files_info = response.json()
        current_app.logger.error(files_info)
        return files_info
    else:
        print(f"Failed to get files. Status code: {response.status_code}, Response: {response.text}")
        return None

def get_info(file_id:str):
    headers = {
    "Authorization": f"Bearer {os.getenv('MOONSHOT_SECRET_KEY')}",
    "Content-Type": "application/json"
    }
    response = requests.get( "https://api.moonshot.cn/v1/files/" + file_id , headers=headers)
    if response.status_code == 200:
        files_info = response.json()
        current_app.logger.error(files_info)
        return files_info
    else:
        print(f"Failed to get files. Status code: {response.status_code}, Response: {response.text}")
        return None
   
def get_info_content(file_id:str):
    
    headers = {
    "Authorization": f'Bearer {os.getenv('MOONSHOT_SECRET_KEY')}',
    "Content-Type": "application/json"
    }
    response = requests.get( "https://api.moonshot.cn/v1/files/" + file_id + '/content' , headers=headers)
    if response.status_code == 200:
        files_info = response.json()
        current_app.logger.error(files_info)
        fileinfo = FileInfo.query.filter_by(moonshot_id=file_id).first()
        current_app.logger.error(fileinfo)
        

        fileinfo.file_content = files_info.get('content', None)
        fileinfo.file_type = files_info.get('file_type', None)
        fileinfo.filename = files_info.get('filename', None)
        fileinfo.title = files_info.get('titleget', None)
        fileinfo.type = files_info.get('type', None)
        db.session.commit()

        return files_info
    else:
        print(f"Failed to get files. Status code: {response.status_code}, Response: {response.text}")
        return None
   

def ask(question:str):
    if question == '':
        return {"message": "请输入问题"}
    question_embedding = text_to_embedding(question)

    text = "三年级一班有同学：小明、小红、大壮、小李、小刚，小红是学习委员、小明是班长，大壮是体育委员和数学课代表。 小红带了红领巾，今天天气小雨，35度，特斯拉卖35万一辆。"
    embedding = text_to_embedding(question)
    answer = chat(question, text)
    qnA_entry = QnA(question=question, embedding=question_embedding.tobytes(), answer=answer)
    db.session.add(qnA_entry)
    db.session.commit()
    
    return answer


def save_data():
    chunks = chunk_text(get_message_b(), 200)
    saveData = []

    for chunk in chunks:
        embedding = text_to_embedding(chunk)
        saveData['words'] = chunk
        saveData['embedding'] = embedding
        saveData['title'] = '一文读懂细胞增殖及毒性检测'
        # qnA_entry = QnA(question=chunk, embedding=embedding.tobytes(), answer=answer)
        # db.session.add(qnA_entry)
        # db.session.commit()


def get_message_b():
    text = """

一、项目介绍


细胞毒性检测是生物相容性测试的一种，检测药物或者新型材料在生物环境中的毒性情况，即通过检测材料或者药物对细胞的增殖或者生长的影响，来评价药物或材料的毒性或者活性，主要用于药物活性筛选、细胞增殖/毒性测定、抗肿瘤药效计算IC50等；常用MTT法或者CCK8法检测，另外也可以通过Live/dead双染法进行细胞成像，更直观的记录细胞的存活情况。


二、实验原理


1.CCK-8测试

CCK-8试剂（Cell Counting Kit-8 细胞计数试剂）中含有WST–8（2-(2-甲氧基-4-硝基苯基)-3-(4-硝基苯基)-5-(2,4-二磺酸苯)-2H-四唑单钠盐），它在电子载体1-甲氧基-5-甲基吩嗪 硫酸二甲酯（1-Methoxy PMS）的作用下被细胞线粒体中的脱氢酶还原为具有高度水溶性的黄色甲臜产物（Formazan），生成的甲臜物的数量与活细胞的数量成正比，用酶联免疫检测仪在450nm波长处测定其光吸收值，可间接反映活细胞数量。注：贴壁细胞和悬浮细胞均可使用此方法，悬浮细胞CCK-8孵育时间应适当延长。



2.MTT测试

活细胞线粒体内的琥珀酸脱氢酶能使外源性MTT还原成水不溶性的蓝紫色结晶甲臜（Formazan）并沉积在细胞中，而死细胞无此功能；二甲基亚砜能溶解细胞中的甲臢，MTT结晶形成的量与细胞数成正比，使用多功能酶标仪在490nm处测定其吸光值，从而定量测定细胞的存活比例。

注：多用于贴壁细胞。  

       

3、Live/Dead细胞染色

活/死细胞双染试剂盒可同时对活细胞和死细胞进行荧光染色。该试剂盒包含钙黄绿素-AM和碘化丙啶(PI)两种溶液，分别用于染色活细胞和死细胞。其中钙黄绿素-AM，即钙黄绿素的乙酰羟甲基酯，具有高度亲脂性和细胞膜透过性。尽管钙黄绿素-AM自身并非荧光分子，但活细胞中的酯酶可以催化钙黄绿素-AM生成钙黄绿素，从而发出强烈的绿色荧光(λex 490 nm, λem 515 nm). 因此钙黄绿素-AM只能染色活细胞。而核染色染料PI不能透过活细胞的细胞膜。但可以透过死细胞膜的变性区域来到达细胞核，并与细胞中的DNA双螺旋结构结合，从而发出红色荧光(λex 535 nm, λem 617 nm)。钙黄绿素和PI-DNA都能被490nm波长的光激发，因此可以采用荧光显微镜同时监测活细胞和死细胞。使用λex激发光时只能观察到死亡细胞。


三、CCK-8与MTT的区别


MTT和CCK8区别主要体现在以下几个方面



综上所述，MTT实验和CCK8实验都是常用的细胞增殖和活性检测方法，它们的选择应根据实验目的和细胞类型进行合理的选择。


四、样品要求


1.液体类

根据测试时样本浓度和检测时间点而定，按照单次检测需要的3-5倍的量寄送；若采用稀释后样本测试，则须告知稀释倍数及工作液浓度；若溶剂为有机溶剂（如DMSO，醇类，酚类等），最高工作液浓度中，溶剂的占比低于0.5%。

2.粉末类

根据测试时样本浓度和检测时间点而定，按照单次检测需要的3-5倍的量寄送；

    a. 可溶性粉末：注明溶剂的种类（如无水乙醇，异丙醇，DMSO，培养基，PBS或者生盐水等），当样品对溶剂有特殊需求时，请在送样时附加所需溶剂；

    b. 不可溶粉末：注明样本性质，灭菌方式，及分散为均匀悬浮液所需必要步骤，

     如果不可使用分散液，需要预试，样本量可跟前期对接技术顾问沟通确认。

3.块体类

    a. 样品与细胞的作用方式为直接接触的话，至少3个/种细胞/时间点；

    b.样本处理方式为浸提的话，可参考国标ISO 10993-12 2007中的浸提方式浸提，根据浸提方式按量和检测时间点提供；

    c.若是需要把细胞接种到材料上的话，金属块、凝胶类样本须制备成统一大小的圆形/方形，建议制备直径为5-7 mm圆形。布料、纸片类样本可代为裁剪，默认制备直径为6 mm。

    注：测试时，默认每组3个平行，每孔培养基加样量100μL

注：以上送样条件仅做参考，具体送样与实验目的和要求相关，具体请联系e测试工作人员。


五、结果展示


1.细胞毒性
将各组吸光度值输入Excel并计算相对活力（相对活力%=（实验组OD值-背景OD值）/（对照组OD值均值-背景OD值）×100），其中背景OD值为只加CCK8/MTT试剂和培养基的吸光度。将相对活力数值输入GraphPad Prism作图，结果如下：



2.细胞死活染色
荧光显微镜，共聚焦可任选其一进行拍摄，一般提供5-6个视野，可选择不同倍数，需要了解详细的结果形式，请联系我们工作人员。

结果如下：




六、注意事项


1、接种细胞数：针对标准96孔板，贴壁细胞的最小接种量为1000个/孔 (100μl培养基)。若为白细胞，接种量不低于2500个/孔 (100μl培养基)。如若使用24孔板或6孔板，应预先计算每孔相应的接种量，并按照每孔培养基总体积的10%加入CCK-8溶液。

2、空白对照：在不含细胞的培养基中加入CCK-8，测定450nm的吸光度即为空白对照。在细胞毒性实验中，还应考虑药物的吸收，可在加入药物的培养基中加入CCK-8，测定450nm的吸光度作为空白对照。

3、第一次做实验时，建议先做几个孔摸索接种细胞的数量和细胞达到实验要求的培养时间，这是因为不同的细胞生长速度不同。

4、培养板周围一圈孔培养液容易挥发，为减少误差，建议培养板周围的四边每孔只加培养基、PBS或水。

5、药物样本初筛时可以适当减少浓度梯度的数量，增大浓度梯度间的倍数。若要确定样本的IC50则需要增加浓度梯度的数量，一般8-12个足矣。若有文献参考，则根据文献设置浓度梯度。

6、加入样本时要注意溶解样本的培养基中血清浓度对样本的影响，部分样本可能受血清影响较大，此时需使用无血清培养基溶解样本。

7、加样本前，要先吸出前面的培养基，但不可长期搁置防止细胞死亡，最好一块板吸完，立即加入配好的不同浓度的样本。

8、Calcein-AM遇到湿气会分解，使用后请在-20度下密闭冷冻保存，防止水分进入。Calcein-AM储备液用缓冲液或培养基等稀释时尽量现配现用。

9、碘化丙啶（PI）有一定的致癌性，操作时一定要注意防护。若接触到皮肤，需要立即用自来水清洗。

本文为e测试原创，未经允许，禁止转载！



"""
   

    return text

def process_message_c():
    # 这里可以加入复杂的业务逻辑处理
    return {"message": "This is endpoint c"}