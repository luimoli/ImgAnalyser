__ViFi_Common__
================= 
## ViFi_Common基础功能函数仓库  

### <center><b>基础信息</b></center>

<br>

### <center><b>依赖库</b></center>  
``` powershell
pip install -r ./requirements.txt
```
    matplotlib==3.6.2
    numpy==1.23.4
    opencv_python==4.6.0.66
    scikit_image==0.19.3  

<br>

### <center><b>代码结构</b></center>
``` 
ViFi_Common
    ├── analysisCommon
    |     └── imgAnalysis.py
    |
    ├── colorCommon
    |     └── imgColorTrans.py
    |
    ├── geometryCommon
    |
    ├── imgCommon
    |     ├── imgChannel.py
    |     ├── imgDistance.py
    |     ├── imgOperator.py
    |     └── imgTrans.py
    |
    ├── metricCommon
    |     └── imgMetrics.py
    |
    ├── videoCommon
    |
    ├── data    
    |     ├── lena_test.png
    |     └── lena.png
    |
    ├── test   
    |                         
    ├── Test.py
    |
    ├── requirements.txt
    |
    └── README.md
```
<br>

### <center><b>现有功能</b></center>
Test.py文件有所有基础功能函数的测试及demo，用于验证函数功能
``` powershell
python Test.py
```
``` python
# 详细参考Test.py
test_diffImgs(imtest, imref) #获得两幅图的差别
test_calcHist(imtest, pleftup, prightdown, roi, mask1) #计算直方图
test_cvtColor(imtest, 'YUV') #色域转换
test_getFDD(imtest) #获得FFT
test_getGrad(imtest) #获得梯度图
test_PerformMask(imtest, mask1) #获得掩膜后的图像
test_PerformROI(imtest, roi) #获得ROI
test_splitChannel(imtest) #分离图像通道
test_Metrics(imtest, imref) #获得图像指标
test_getDis(imtest, pleftup, prightdown) #获得图像点之间的距离
```
<br>

### <center><b>接口定义</b></center>  

| 参数 | 数据类型 | 例子  | 说明 |
| :--- | :--- | :---: | :---: |
| **point** | list | [100, 100] | 和opencv中[h, w]的形式保持一致 |
| **mask** | np.array |  | 一般为0，1整型Mask， 也支持[0,1]浮点数Mask<br>支持不同channel使用不同的Mask |
| **roi** | list[list, ] | [[100, 100], [200, 200]] |  [p1, p2], p1和p2分别为leftup和rightdown |
| **img** | np.array |  | uint8， uint16的BGR形式数据， <br>即cv2.imread(src, cv2.IMREAD_UNCHANGED) |
<br>


----------
* Author: yufei.zhang@smartmore.com  
* Date: 2022.01.03  


