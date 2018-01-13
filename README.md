# hq-answer-assist
HQ类答题游戏辅助（python）

## 项目介绍

如百万英雄、冲顶大会、芝士超人等HQ类答题游戏辅助，可帮你搜索并匹配答案。原理同前一阵大火的[跳一跳辅助](https://github.com/wangshub/wechat_jump_game)类似，将答题页面截图，然后使用图片识别功能转成文字，再放到百度去搜索。

截图使用的是adb,所以目前仅支持android。图片识别使用 [tesseract-orc](https://github.com/tesseract-ocr/tesseract)。

具体思路如下：

1. 答题时使用adb截图并将图片pull到本机
2. 通过ocr图片识别题目
3. 百度题目
4. 百度后结果与选项做匹配，匹配度最高的即为推荐答案


## 项目结构

```
--- hq-answer-assist(根目录)

   --- config(屏幕分辨率配置目录)

   --- image （图片目录）
  
   --- .gitignore
  
   --- analyze.py (文字识别功能)
   
   --- baiduocr.py (百度OCR集成)
  
   --- config.json(配置文件)
  
   --- LICENSE
  
   --- main.py(主函数)
  
   --- README.md
   
   --- search.py(搜索函数)
   
   --- utils.py (工具函数)
  
```



## 使用说明

使用该脚本需保证以下环境安装

1. python运行环境
2. android调试工具[ADB](https://developer.android.com/studio/command-line/adb.html?hl=zh-cn),安装Android SDK后可在android_sdk/platform-tools/中找到。其他安装方式百度即可。
3. python若干类库：PIL(图片库)、BeautifulSoup(网页解析库)、pytesseract（图片文字识别库）、baidu-aip（百度ocr库）。可使用python的pip安装
4. 文字识别引擎（可选,若使用百度云OCR可不安装）[tesseract-ocr](https://github.com/tesseract-ocr/tesseract)及中文简体语言包[chi_sim.traineddata](https://github.com/tesseract-ocr/tessdata/blob/master/chi_sim.traineddata),
安装教程可百度，Mac安装教程[在这里](http://blog.csdn.net/u010670689/article/details/78374623),其他系统可做参考。


已集成百度OCR,识别效果比不经训练的tesseract-ocr要准确。需在百度云创建应用，具体见[百度云文字识别文档](https://cloud.baidu.com/doc/OCR/OCR-Python-SDK.html#.E9.85.8D.E7.BD.AEAipOcr)
使用百度云OCR需在配置文件`config.json`中配置如下：

```json
{
  "auto": true,
  "baidu_ocr": true,  //  启用百度云OCR
  "baidu_ocr_config": { //  百度云OCR配置 
    "app_id": "xxx",
    "api_ley": "xxx",
    "secret_key": "xxx"
  }
}
```


答题时使用USB线连接PC,开启调试模式。目前有两种运行方式：手动和自动。默认为自动。配置在`config.json`中。将`auto`设置`false`则为手动。

### 手动

每次手机画面出现答题页面，手动执行`python3 main.py`命令。

### 自动

直接运行`python3 main.py`即可。程序会自主判断是否为答题页面。判断成功后自动图片识别并搜索。搜索出答案后停留10秒继续循环判断。目前每0.5秒判断一次。


## 结果展示

对知识性的问题准确率是很高的。

![](http://blog.wthfeng.com/img/posts/resource/answer/answer1.png)

![](http://blog.wthfeng.com/img/posts/resource/answer/answer2.png)

![](http://blog.wthfeng.com/img/posts/resource/answer/answer3.png)

虽然题目没有百分百识别成功，不过只要有主要关键字即可。



## 适配支持

屏幕分辨率适配在`config/`目录下，目前支持`540x960`、`720x1280`、`1080x1920`等分辨率。若没有你手机的分辨率。可在此目录下添加对应文件。格式如下

```json

{
  // 题目及选项区域，(x1,y1)为左上点左边，(x2,y2)为右下点坐标，由此组成的矩形区域
  "question_area": {
    "x1": 23,
    "y1": 150,
    "x2": 510,
    "y2": 600
  },
  // 答题页面上方特有的白条区域，用于判断是否为答题页面
  "blank_area": {
    "x1": 75,
    "y1": 150,
    "x2": 450,
    "y2": 600
  }
}

```
`blank_area`表示的区域如下所示：


![](http://blog.wthfeng.com/img/posts/resource/answer/answer4.png)





## 其他补充


tesseract识别文字偶尔会有误差。可训练以提高。

另由于题目本身原因，部分可能搜索不到答案或搜索有误，需自己留意那些奇怪的问题。

如果你遇到任何问题，可提[Issues](https://github.com/wangtonghe/hq-answer-assist/issues)

如果你有更好的思路，欢迎分享讨论。欢迎贡献代码PR。

