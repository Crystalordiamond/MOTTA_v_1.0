
//旧柱状图
function setBardata(id,name,user,mod,data)
{

    var myChart;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart= echarts.init(main);
    }


        var dataValue=new Date();
        var value=[];
        var listValue=[];

        if(data!=undefined)
        {
            listValue=data.listValue;
        }


        if(mod==1)
        {
            for(var l=0;l<31;l++){

              value.push(l+1);

            }
        }else if(mod==2)
        {
            for(var l=0;l<12;l++){

                value.push(l+1);

            }
        }else
        {

            for(var l=0;l<10;l++){

                value.push(dataValue.getFullYear()-5+l);

            }

        }


        // 指定图表的配置项和数据
        var option = {
			
			color: ['#3398DB'],
			
            title: {
                text: ''
            },
            tooltip: {},
            legend: {
                data:[name],
                x: 'left',
            },
            xAxis: {
                data: value
            },
            yAxis: {},
            series: [{
                name: name,
                type: 'bar',
                data: listValue
            }]
        };

        // 使用刚指定的配置项和数据显示图表。
        myChart.setOption(option);
}



//实时柱状图
function setOldBardata(id,name,user) {

    var myChart;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart = existInstance;
        }
    } else {
        // 基于准备好的dom，初始化echarts实例
        myChart = echarts.init(main);
    }


    var value = user.strList;
    var listValue = user.cList;
    var colorValue=user.colorList;
    var dataLable=user.dataLable;

    // 指定图表的配置项和数据
    var option = {

        color: colorValue,

        title: {
            text: ''
        },
        tooltip: {},
        legend: {
            data: dataLable,
            x: 'left',
        },
        xAxis: {
            data: value,
            axisLine: {
                show: true,
                lineStyle: {
                    color:user.scaleColor
                }
            },
        },
        yAxis: {

            axisLine: {
                show: true,
                lineStyle: {
                    color:user.scaleColor
                }
            }

        },
        series: [{
            name: dataLable,
            type: 'bar',
            data: listValue
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//新柱状图
function setNewBardata(id,name,user,mod)
{

    var myChart;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart= echarts.init(main);
    }
    var dataValue=new Date();
    var value=[];
    var listValue=[];
    var dataLable=user.dataLable;
	
    if(mod==1)
    {
        for(var l=0;l<31;l++){

            value.push(l+1);

        }
        listValue=user.dList;
    }else if(mod==2)
    {
        for(var l=0;l<12;l++){

            value.push(l+1);

        }
        listValue=user.mList;
    }else
    {

        for(var l=0;l<10;l++){

            value.push(user.startYear+l);

        }
        listValue=user.yList;

    }


    // 指定图表的配置项和数据
    var option = {

        color: user.colorList,

        title: {
            text: ''
        },
        tooltip: {},
        legend: {
            data:dataLable,
            x: 'left',
        },
        xAxis: {
            data: value,
            splitLine: {
                show: false,

            },
            axisLine: {
                show: true,
                lineStyle: {
                    color:user.fontColor
                }
            },
        },
        yAxis: {
            splitLine: {
                show: false,

            },
            axisLine: {
                show: true,
                lineStyle: {
                    color:user.fontColor
                }
            },
        },
        series: [{
            name: dataLable,
            type: 'bar',
            data: listValue
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//折线图
function setLinedata(id,user,mod)
{


    var data=[];


    if(mod=='h')
    {

        for(var x in user.mapHvlaue){

            var m=[];
            m.push(x/60,user.mapHvlaue[x]);
            data.push(m);
        }

    }else if(mod=='d'){

        for(var x in user.mapDvlaue){

            var m=[];
            m.push(x/60,user.mapDvlaue[x]);
            data.push(m);
        }


    }else if(mod=='m'){

        for(var x in user.mapMvlaue){

            var m=[];
            m.push(x,user.mapMvlaue[x]);
            data.push(m);
        }

    }else if(mod=='y'){

        for(var x in user.mapYvlaue){

            var m=[];
            m.push(x,user.mapYvlaue[x]);
            data.push(m);
        }

    }




    var myChart2;
   // var main = document.getElementById(id);
   // var main = $('#'+id)[0];
    var main=document.getElementById(id);

    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart2=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart2= echarts.init(main);
    }
        // 指定图表的配置项和数据
    var option2 = {
    xAxis: {
        type: 'value',
    },
	
    yAxis: {
        type: 'value'
    },
	
	 legend: {
                data:[''],
            },
	
    series: [{
		
		
		color: '#3398DB',
		name: '',
        data: data,
        type: 'line',
        smooth: true
		
    }]
};
        // 使用刚指定的配置项和数据显示图表。
        myChart2.setOption(option2);
}



//曲线图
function setLineChart(id,user,mod)
{



    var mdata=user.ldata;

    var datas=[];
    var data={};


  //  alert(JSON.stringify(mdata[4]));

    if(mod=='时')
    {



        for(var h=0; h<mdata[1].length;h++){

            var datah=[];
            for(var x in mdata[1][h])
            {
                var m=[];
                m.push(x,mdata[1][h][x]);
                datah.push(m);
            }
            data[h]=datah;

        }


    }
    else if(mod=='日'){

        for(var h=0; h<mdata[2].length;h++){

            var datah=[];
            for(var x in mdata[2][h])
            {
                var m=[];
                m.push(x,mdata[2][h][x]);
                datah.push(m);
            }
            data[h]=datah;
    }
    }
   else if(mod=='月'){

        for(var h=0; h<mdata[3].length;h++){

            var datah=[];
            for(var x in mdata[3][h])
            {
                var m=[];
				
				var vs=parseFloat(x)+1;
				
                m.push(vs,mdata[3][h][x]);
                datah.push(m);
            }

            data[h]=datah;
    }

    }
    else if(mod=='年'){

        for(var h=0; h<mdata[4].length;h++){

            var datah=[];

            for(var x in mdata[4][h])
            {
                var m=[];
				var vs=parseFloat(x)+1;
				
					
                m.push(vs,mdata[4][h][x]);
                datah.push(m);

            }

            data[h]=datah;

    }
    }

   //
   //
   //
    for(var i=0; i<user.lableList.length; i++){



            var v={};
            v['name']=user.lableList[i];
            v['data']=data[i];
            v['type']='line';
            v['color']=user.colorData[i];
            v['smooth']=true;

            datas.push(v);



    }




    var myChart2;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart2=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart2= echarts.init(main);
    }

    option = {



        xAxis: {
            type: 'value',
           // data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            axisTick: {
                show: false
            },
            axisLine: {
                show: true,
                lineStyle: {
                    color:user.xColor
                }
            },
            axisLabel: {
                show: true,
                color: user.fontColor
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: ['transparent'],
                }
            },
        },
        yAxis: {

            color: user.xColor,
            type: 'value',
            axisTick: {
                show: false
            },
            axisLine: {
                show: true,
                lineStyle: {
                    color:user.xColor
                }
            },
            axisLabel: {
                show: true,
                color: user.fontColor
            },
            splitLine: {
                show: true,
                lineStyle: {
                    color: [user.scaleColor],
                }
            },
        },

        legend: {
            data:user.lableList,
        },

         series:datas

    };

    // 使用刚指定的配置项和数据显示图表。
    myChart2.setOption(option);
}


//饼图
function setPiedata(id,user)
{

    var myChart3;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart3=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart3= echarts.init(main);
    }


    var data=[];


    for(var i=0;i<user.textData.length;i++)
    {
        var list={};
        list['value']=user.dataList[i];
        list['name']=user.textData[i];

        var itemStyle={};
        var normal={};
        normal['color']=user.colorData[i];
        itemStyle['normal']=normal;
        list['itemStyle']=itemStyle;


        data.push(list);

    }

        // 指定图表的配置项和数据
    var option3 = {
    title : {
        text: '',
        subtext: '',
        x:'center'
    },
    tooltip : {
        trigger: 'item',
        formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        left: 'left',
        data: user.textData,
        textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
            color: 'auto'
        }
    },
    series : [
        {
            name: '访问来源',
            type: 'pie',
            radius : '55%',
            center: ['50%', '60%'],
            data:data,
            itemStyle: {
                emphasis: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            }
        }
    ]
};
        // 使用刚指定的配置项和数据显示图表。
        myChart3.setOption(option3);
}


//仪表盘1
function setGrdata(id,name,min,max,value,warmPer,borderColor,fillColor,lineColor,backgroundColor,warmPerColor)
{




    var myChart4;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart4=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart4= echarts.init(main);
    }

        // 指定图表的配置项和数据
       var 		option4 = {
       tooltip : {
           formatter:""
       },
       series: [
        {
			min:min,
            max:max,
            name: '',
            type: 'gauge',
            detail: {
                show : false,
			    formatter:'{value}',
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    color: 'auto',
                    fontWeight: 'bolder'
                }
            },
			
		    axisLine: {            // 坐标轴线
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: [[warmPer,borderColor],[1, warmPerColor]],
                    width: 10,
                    shadowColor : '#fff', //默认透明
                    shadowBlur: 10
                }
            },
            axisLabel: {           // 坐标轴文本标签，详见axis.axisLabel
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    color: 'auto'
                }
            },
            axisTick: {            // 坐标轴小标记
                splitNumber: 10,   // 每份split细分多少段
                length :12,        // 属性length控制线长
                lineStyle: {       // 属性lineStyle控制线条样式
                    color: 'auto'
                }
            },
            pointer : {           //指针宽度  指针颜色和表盘圆环颜色一致。
                width : 5
            },
            title : {
                show : false,
                offsetCenter: [0, '-40%'],       // x, y，单位px
                textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder'
                }
            },
			
			 splitLine: {           // 分隔线
                length :15,         // 属性length控制线长
                // lineStyle: {        // 属性lineStyle（详见lineStyle）控制线条样式
                //     width:3,
                //     color: '#fff',
                //     shadowColor : '#fff', //默认透明
                //     shadowBlur: 10
                // }
            },
            
			
			
            data: [{value: value, name: name}]
        }
    ]
};

        // 使用刚指定的配置项和数据显示图表。
        myChart4.setOption(option4);
		

}


//仪表盘2
function setGrdata2(id,name,min,max,value,listValue,listColor)
{



    var myChart4;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart4=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart4= echarts.init(main);
    }

    var a=listValue[0]/180;

    // 指定图表的配置项和数据
    var 	option4 = {
        tooltip : {
            formatter:""
        },
        series: [
            {
                min:min,
                max:max,
                name: '',
                type: 'gauge',
                detail: {
                    show : false,
                    formatter:'{value}',
                    textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                        color: 'auto',
                        fontWeight: 'bolder'
                    }
                },

                axisLine: {            // 坐标轴线
                    lineStyle: {       // 属性lineStyle控制线条样式
                        color: [[a,listColor[0]],[1, listColor[1]]],
                        width: 10,
                        shadowColor : '#fff', //默认透明
                        shadowBlur: 10
                    }
                },
                axisLabel: {           // 坐标轴文本标签，详见axis.axisLabel
                    textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                        color: 'auto'
                    }
                },
                // axisTick: {            // 坐标轴小标记
                //     splitNumber: 10,   // 每份split细分多少段
                //     length :12,        // 属性length控制线长
                //     lineStyle: {       // 属性lineStyle控制线条样式
                //         color: 'auto'
                //     }
                // },
                pointer : {           //指针宽度  指针颜色和表盘圆环颜色一致。
                    width : 5,
                    color : '#fff'
                },
                // title : {
                //     show : false,
                //     offsetCenter: [0, '-40%'],       // x, y，单位px
                //     textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                //         fontWeight: 'bolder'
                //     }
                // },

                splitLine: {           // 分隔线
                    length :10,         // 属性length控制线长
                    // lineStyle: {        // 属性lineStyle（详见lineStyle）控制线条样式
                    //    width:3,
                    //    color: '#fff',
                    //    shadowColor : '#fff', //默认透明
                    //    shadowBlur: 5
                    // }
                },



                data: [{value: value, name: name}]
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart4.setOption(option4);


}


//圆环
function setCriData(id,user)
{

    var myChart;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart= echarts.init(main);
    }

    var bg=user.lineColor;
    var fill="#fff";
    var warF=user.warmPer;
    var value=user.value;
    if(warF>value)
    {
        fill=user.fillColor;
    }else
    {
        fill=user.warmPerColor;
    }

	var option = {
    title: {
        show:false,
        text: '80%',
        x: 'center',
        y: 'center',
        textStyle: {
            fontWeight: 'normal',
            color: '#0580f2',
            fontSize: '25'
        }
    },
    color: ['rgba(176, 212, 251, 1)'], 
    legend: {
        show: false,
        itemGap: 12,
        data: [name, '02']
    },
   
    series: [{
        name: 'Line 1',
        type: 'pie',
        clockWise: true,
        radius: ['50%', '66%'],
        itemStyle: {
            normal: {
                label: {
                    show: false
                },
                labelLine: {
                    show: false
                }
            }
        },
        hoverAnimation: false, 
        data: [{
            value: value,
            name: name,
            itemStyle: {
                normal: {
                    color: { // 完成的圆环的颜色
                        colorStops: [{
                            offset: 0,
                            color: fill // 0% 处的颜色#367bec
                        }, {
                            offset: 1,
                            color: bg // 100% 处的颜色
                        }]
                    },
                    label: {
                        show: false
                    },
                    labelLine: {
                        show: false
                    }
                } 
            }
        }, {
            
            value: 100-value
        }]
    }]
    };
	
	 myChart.setOption(option);
}

//温度计
function setWenduJi(id,values)
{


    var myChart;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart= echarts.init(main);
    }




	var value =values;
    var kd = [];

console.log(kd)

var data = getData(value);
var mercuryColor = '#fd4d49';
var borderColor = '#fd4d49';

option = {
    title: {
        text: '温度计',
        show: false
    },
    yAxis: [{
        show: false,
        min: 0,
        max: 130,
    }, {
        show: false,
        data: [],
        min: 0,
        max: 130,
    }],
    xAxis: [{
        show: false,
        data: []
    }, {
        show: false,
        data: []
    }, {
        show: false,
        data: []
    }, {
        show: false,
        min: -110,
        max: 100,

    }],
    series: [{
        name: '条',
        type: 'bar',
        // 对应上面XAxis的第一个对象配置
        xAxisIndex: 0,
        data: data,
        barWidth: 8,
        itemStyle: {
            normal: {
                color: mercuryColor,
                barBorderRadius: 0,
            }
        },
        label: {
            normal: {
                show: true,
                position: 'right',
                formatter: function(param) {
                    // 因为柱状初始化为0，温度存在负值，所以，原本的0-100，改为0-130，0-30用于表示负值
                     return data+ '°C';
                },
                textStyle: {
                    color: '#ccc',
                    fontSize: '10',
                }
            }
        },
        z: 2
    }, {
        name: '白框',
        type: 'bar',
        xAxisIndex: 1,
        barGap: '-100%',
        data: [129],
        barWidth: 13,
        itemStyle: {
            normal: {
                color: '#ffffff',
                barBorderRadius: 10,
            }
        },
        z: 1
    }, {
        name: '外框',
        type: 'bar',
        xAxisIndex: 2,
        barGap: '-100%',
        data: [130],
        barWidth: 15,
        itemStyle: {
            normal: {
                color: borderColor,
                barBorderRadius: 20,
            }
        },
        z: 0
    }, {
        name: '圆',
        type: 'scatter',
        hoverAnimation: false,
        data: [0],
        xAxisIndex: 0,
        symbolSize: 15,
        itemStyle: {
            normal: {
                color: mercuryColor,
                opacity: 1,
            }
        },
        z: 2
    }, {
        name: '白圆',
        type: 'scatter',
        hoverAnimation: false,
        data: [0],
        xAxisIndex: 1,
        symbolSize: 18,
        itemStyle: {
            normal: {
                color: '#ffffff',
                opacity: 1,
            }
        },
        z: 1
    }, {
        name: '外圆',
        type: 'scatter',
        hoverAnimation: false,
        data: [0],
        xAxisIndex: 2,
        symbolSize: 20,
        itemStyle: {
            normal: {
                color: borderColor,
                opacity: 1,
            }
        },
        z: 0
    }, {
        name: '刻度',
        type: 'bar',
        yAxisIndex: 1,
        xAxisIndex: 3,
        label: {
            normal: {
                show: true,
                position: 'right',
                distance: 5,
                color: '#525252',
                fontSize: 10,
                formatter: function(params) {
                    // 因为柱状初始化为0，温度存在负值，所以，原本的0-100，改为0-130，0-30用于表示负值
                    if (params.dataIndex > 100 || params.dataIndex < 30) {
                        return '';
                    } else {
                        if (params.dataIndex % 5 === 0) {
                            return params.dataIndex - 30;
                        } else {
                            return '';
                        }
                    }
                }
            }
        },
        barGap: '-100%',
        data: kd,
        barWidth: 1,
        itemStyle: {
            normal: {
                color: borderColor,
                barBorderRadius: 5,
            }
        },
        z: 0
    }]
};
	
	 myChart.setOption(option);
}

// 因为柱状初始化为0，温度存在负值，所以，原本的0-100，改为0-130，0-30用于表示负值
function getData(value) {
    return [value + 30];
}




function setStackLineData(id)
{
    var myChart4;
    var main = document.getElementById(id);
    var existInstance = echarts.getInstanceByDom(main);
    if (existInstance) {
        if (true) {
            //existInstance.dispose();
            myChart4=existInstance;
        }
    }else
    {
        // 基于准备好的dom，初始化echarts实例
        myChart4= echarts.init(main);
    }

    var option = {
    title: {
        text: '',
        left: '50%',
        textAlign: 'center'
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            lineStyle: {
                color: '#ddd'
            }
        },
        backgroundColor: 'rgba(255,255,255,1)',
        padding: [5, 10],
        textStyle: {
            color: '#7588E4',
        },
        extraCssText: 'box-shadow: 0 0 5px rgba(0,0,0,0.3)'
    },
    legend: {
        right: 20,
        orient: 'vertical',
        data: ['温度','湿度']
    },
    xAxis: {
        type: 'category',
        data: ['00:00','2:00','4:00','6:00','8:00','10:00','12:00','14:00','16:00','18:00','20:00',"22:00"],
        boundaryGap: false,
        splitLine: {
            show: false,
            interval: 'auto',
            lineStyle: {
                color: ['#D4DFF5']
            }
        },
        axisTick: {
            show: false
        },
        axisLine: {
            lineStyle: {
                color: '#609ee9'
            }
        },
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14
            }
        }
    },
    yAxis: {
        type: 'value',
        splitLine: {
            show: false,
            lineStyle: {
                color: ['#D4DFF5']
            }
        },
        axisTick: {
            show: false
        },
        axisLine: {
            lineStyle: {
                
                color: '#609ee9'
            }
        },
        axisLabel: {
            margin: 10,
            textStyle: {
                fontSize: 14
            }
        }
    },
    series: [{
        name: '出风温度',
        type: 'line',
        smooth: true,
        showSymbol: false,
        symbol: 'circle',
        symbolSize: 6,
        data: ['30', '20', '25', '27', '21', '34', '33', '32', '36', '37', '38', '45'],
        areaStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(199, 237, 250,0.5)'
                }, {
                    offset: 1,
                    color: 'rgba(199, 237, 250,0.2)'
                }], false)
            }
        },
        itemStyle: {
            normal: {
                color: '#f7b851'
            }
        },
        lineStyle: {
            normal: {
                width: 1
            }
        }
    }, {
        name: '进风温度',
        type: 'line',
        smooth: true,
        showSymbol: false,
        symbol: 'circle',
        symbolSize: 6,
        data: ['50', '60', '45', '35', '70', '56', '65', '74', '67', '80', '69', '90'],
        areaStyle: {
            normal: {
                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                    offset: 0,
                    color: 'rgba(216, 244, 247,1)'
                }, {
                    offset: 1,
                    color: 'rgba(216, 244, 247,1)'
                }], false)
            }
        },
        itemStyle: {
            normal: {
                color: '#58c8da'
            }
        },
        lineStyle: {
            normal: {
                width: 1
            }
        }
    }]
};
	
	 myChart.setOption(option);
}