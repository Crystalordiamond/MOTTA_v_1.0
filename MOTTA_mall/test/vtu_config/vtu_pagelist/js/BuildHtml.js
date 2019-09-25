
//初始化控件
function init(user,type,typeId, pos,index, x, y, h, w){

    switch(type)
    {

        case "Label":


            $("div.Main").append("  <font  class='Label'></font>  ");
            $('font.Label').removeClass("Label").addClass(typeId);


            if(user.cmd!=undefined&&user.cmd!="") {

                $('font.' + typeId).text(user.value);
            }else
            {
                $('font.'+typeId).text(user.text);
            }

            //$('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":user.textSize,"height":h,"width":w,'text-align':'center','color':user.textColor,'line-height':h+'px'});
            $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":user.textSize*window.screen.availWidth/user.fromWight,"height":h,"width":w,'text-align':user.duiqiWay,'color':user.textColor,'line-height':h+'px'});

            break;
        case "Rectangle":

            $("div.Main").append("  <div  class='Label'></div>  ");
            $('div.Label').removeClass("Label").addClass(typeId);

            var bColor;
            if(user.borderColor=="#FFFFFFFF")
            {
                bColor='transparent';
            }else
            {
                bColor=user.borderColor;
            }

            if(user.bgColor=="#FFFFFFFF")
            {
                $('div.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"background-color":"transparent","height":h,"width":w,'border':'solid '+user.borderWidth+'px '+bColor});
            }else{


                $('div.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"background-color":user.bgColor,"height":h,"width":w,'border':'solid '+user.borderWidth+'px '+bColor});

                if(user.alpha!=0)
                {
                    $('div.'+typeId).css({"opacity":user.alpha/255});
                }

            }

            break;

        case "Image":



            $("div.Main").append("  <a class='Label'><img  class='Label' alt='fail'/></a>  ");
            $('img.Label').removeClass("Label").addClass(typeId);
            $('a.Label').removeClass("Label").addClass(typeId);
            $('img.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"alt":'fali',"height":h,"width":w});
            $('img.'+typeId).attr("src",user.imagePath);

            if(user.hrefUrl!=undefined)
            {
                $('a.'+typeId).attr("href",user.hrefUrl+".html");
            }

            if(user.onClickEvent=="隐藏")
            {
                $('img.'+typeId).hide();
            }




            break;

        case "Table":



            $("div.Main").append(" <table class='Table' > </table> ");
            $("table.Table").removeClass("Table").addClass(typeId);
            $("table."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w});
            $("table."+typeId).attr("borderColor",user.lineColor);
            $("table."+typeId).attr("border","1px");
            $("table."+typeId).attr("cellspacing","0");



            for(var i=0;i<user.rowNUm;i++)
            {
                $("table."+typeId).append("<tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);

                for(var j=0;j<user.colNum;j++)
                {
                    $("tr."+typeId+'Tr'+i).append("<td class='Td'></td>");

                    var classNames=typeId+'Td'+i+''+j;
                    $("td.Td").removeClass("Td").addClass(classNames);
                    $("td."+classNames).attr("bordercolor",user.lineColor);
                    if(i==0) {

                        $("td."+classNames).css({"height":user.firstRow*h});

                    }else
                    {
                        $("td."+classNames).css({"height":(h-user.firstRow*h)/(user.rowNUm-1)});
                    }


                    if(j==0)
                    {

                        $("td."+classNames).css({"width":user.firstCol*w});
                    }else {
                        $("td."+classNames).css({"width":(w-user.firstCol*w)/(user.colNum-1)});
                    }

                }
            }




            break;

        case "Button":

            // alert("Button"+typeId+" "+user.text+" "+user.textColor+" "+user.textSize+" "+user.hrefUrl+".html")


            $("div.Main").append(" <a class='Button'><input type='button' class='Button'/> </a>");
            $("a.Button").removeClass("Button").addClass(typeId);
            $("input.Button").removeClass("Button").addClass(typeId);




            if(user.click==true)//如果按钮有点击事件
            {
                $('input.'+typeId).click(function () {


                    var title=$(document).attr('title');


                    $.ajax({
                        url :  "onClick",	//请求url
                        type : "POST",	//请求类型  post|get
                        data : "titleName="+title+"&typeId="+typeId,	//后台用 request.getParameter("key");
                        dataType : "json",  //返回数据的 类型 text|json|html--
                        success : function(users){	//回调函数 和 后台返回的 数据



                        }
                    });

                });

            }




            $('input.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w,"background-size":"100% 100%"});
            $("input."+typeId).css({"color":user.textColor,"font-size":user.textSize});
            $("input."+typeId).attr('value',user.text);

            if(user.imgSrc!=undefined&&user.imgSrc!="")
            {
                $("input."+typeId).css("background-image","url("+user.imgSrc+")");
            }

            if(user.hrefUrl!=undefined)
            {
                $('a.'+typeId).attr("href",user.hrefUrl+".html");
            }



            break;



        case "EventList":




            $("div.Main").append(" <div   class='EventList' > <div/> ");
            $("div.EventList").removeClass("EventList").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y-20,"height":h+20,"width":w,"overflow-y": "scroll"});
            $("div."+typeId).append(" <table class='EventList' > </table> ");
            $("table.EventList").removeClass("EventList").addClass(typeId);
            $("table."+typeId).attr("cellspacing","1");
            $("table."+typeId).attr("align","center");

            for(var i=-1;i<user.data.length;i++)
            {
                $("table."+typeId).append(" <tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                if(i%2==0)
                {
                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.evenRowBackground});
                    }

                }else
                {

                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.oddRowBackground});
                    }

                }

                for(var j=0;j<5;j++)
                {
                    if(i==-1)
                    {

                        $("tr."+typeId+'Tr'+i).append("<td class='Td'>设备名称</td>");
                        
                    }else
                    {

                        $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");

                    }

                    var caa=typeId+'Td'+i+''+j;
                    $("td.Td").removeClass("Td").addClass(caa);
                    $("td."+caa).css({"width":user.wight/user.fromWight*window.screen.availWidth/5});
                    $("td."+caa).css({"text-align":'center'});
                    if(i!=-1)
                    {
                        $("td."+caa).html(user.data[i][j]);
                    }else {

                        $("td."+caa).html(user.lstTitles[j]);
                    }



                }
            }


            break;

        case "Dial_C":

            //alert(user.warmpercolor+" "+user.warmperColor+" "+user.warmPerColor);
            $("div.main").append("<div class='Dial_C'></div>")
            $("div.Dial_C").removeClass("Dial_C").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x-((1.2-1)*w)/2,"top":y-((1.2-1)*h)/2,"height":h*1.2,"width":w*1.2})
            $("div."+typeId).attr('id',typeId);
            setGrdata(typeId,"",user.minValue,user.maxValue,user.value,user.warmPer,user.borderColor,user.fillColor,user.lineColor,user.backgroundColor,user.warmPerColor);

            break;

        case "SignalList":


            //alert("SignalList："+user.foreColor+"."+user.evenRowBackground+"."+user.oddRowBackground);
            $("div.Main").append(" <div   class='SignalList' > <div/> ");
            $("div.SignalList").removeClass("SignalList").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y-20,"height":h+20,"width":w,"overflow-y": "scroll"});
            $("div."+typeId).append(" <table class='SignalList' > </table> ");
            $("table.SignalList").removeClass("SignalList").addClass(typeId);
            $("table."+typeId).attr("cellspacing","1");
            $("table."+typeId).attr("align","center");

            for(var i=-1;i<user.data.length;i++)
            {
                $("table."+typeId).append(" <tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                if(i%2==0)
                {
                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.evenRowBackground});
                    }

                }else
                {

                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.oddRowBackground});
                    }

                }

                for(var j=0;j<5;j++)
                {
                  
  				   //if(i==-1)
                  //  {
                   //     $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");

                   // }else
                  //  {

                  //      $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");

                  //  }
					 $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");

                    var caa=typeId+'Td'+i+''+j;
                    $("td.Td").removeClass("Td").addClass(caa);
                    $("td."+caa).css({"width":user.wight/user.fromWight*window.screen.availWidth/5});
                    $("td."+caa).css({"text-align":'center'});
                    if(i!=-1)
                    {
                        $("td."+caa).html(user.data[i][j]);
                    }else
                    {
                        $("td."+caa).html(user.lstTitles[j]);
                    }



                }
            }


            break;

        case "AutoSigList":




            $("div.main").append("<div class='AutoSigList' ></div>")
            $("div.AutoSigList").removeClass("AutoSigList").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w});
            $("div."+typeId).attr('id',typeId);



            $("div.main").append("<input type='radio' class='AutoSigList' checked='checked' value='h' /><font class='AutoSigList'>hour</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"h");
            $("input."+typeId+"h").attr("name",typeId);
            $("input."+typeId+"h").css({"position":pos,'z-index':index,"left":x,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"h");
            $("font."+typeId+"h").css({"position":pos,'z-index':index,"left":x+w/8+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"h").click(function () {




                map[typeId] = $("input."+typeId+"h").val();

                setLinedata(typeId,user,map[typeId]);


            });

            $("div.main").append("<input type='radio' class='AutoSigList' value='d'/><font class='AutoSigList'>day</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"d");
            $("input."+typeId+"d").attr("name",typeId);
            $("input."+typeId+"d").css({"position":pos,'z-index':index,"left":x+w/4,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"d");
            $("font."+typeId+"d").css({"position":pos,'z-index':index,"left":x+w*3/8+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"d").click(function () {


                map[typeId] = $("input."+typeId+"d").val();

                setLinedata(typeId,user,map[typeId]);

            });

            $("div.main").append("<input type='radio'  class='AutoSigList' value='m'/><font class='AutoSigList'>mon</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"m");
            $("input."+typeId+"m").attr("name",typeId);
            $("input."+typeId+"m").css({"position":pos,'z-index':index,"left":x+w/2,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"m");
            $("font."+typeId+"m").css({"position":pos,'z-index':index,"left":x+w*5/8+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"m").click(function () {

                map[typeId] = $("input."+typeId+"m").val();

                setLinedata(typeId,user,map[typeId]);

            });

            $("div.main").append("<input type='radio' class='AutoSigList' value='y'/><font class='AutoSigList'>year</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"y");
            $("input."+typeId+"y").attr("name",typeId);
            $("input."+typeId+"y").css({"position":pos,'z-index':index,"left":x+w*3/4,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"y");
            $("font."+typeId+"y").css({"position":pos,'z-index':index,"left":x+w*7/8+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"y").click(function () {

                map[typeId] = $("input."+typeId+"y").val();
                setLinedata(typeId,user,map[typeId]);
            });


            map[typeId] = 'h';
            setLinedata(typeId,user, map[typeId]);

            break;

        case "tigerLabel":


        $("div.Main").append("  <font  class='tigerLabel'></font>  ");
        $('font.tigerLabel').removeClass("tigerLabel").addClass(typeId);



        if(user.cmd!=undefined&&user.cmd!="") {

            $('font.' + typeId).text(user.value);
        }else
        {
            $('font.'+typeId).text(user.text);
        }

        $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":user.textSize,"height":h,"width":w,'text-align':'center','color':user.textColor,'line-height':h+'px'});

        break;


        case "AlarmLight":

           $("div.Main").append("  <img  class='AlarmLight' alt='fail'/>  ");
            $('img.AlarmLight').removeClass("AlarmLight").addClass(typeId);
            $('img.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"alt":'fali',"height":h,"width":w});
            if(user.value==0)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel1.png');

            }else if(user.value==1)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel1.png');
            }else if(user.value==2)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel2.png');
            }else if(user.value==3)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel3.png');
            }else if(user.value==4)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel4.png');
            }

            break;

        case "YTParameter":

            $("div.Main").append("  <input type='text' class='YTParameter' />  ");
            $('input.YTParameter').removeClass("YTParameter").addClass(typeId+'text');
            $('input.'+typeId+'text').css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w*0.7});



            $("div.Main").append("  <input type='button' class='YTParameter' />  ");
            $('input.YTParameter').removeClass("YTParameter").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+0.71*w,"top":y,"height":h,"width":w*0.29});
            $("input."+typeId+'button').attr('value',user.content);
            $("input."+typeId+'button').attr('color',user.fontColor);


            if(user.click==true)//如果按钮有点击事件
            {
                $('input.'+typeId+'button').click(function () {


                    var title=$(document).attr('title');


                    $.ajax({
                        url :  "onClick",	//请求url
                        type : "POST",	//请求类型  post|get
                        data : "titleName="+title+"&typeId="+typeId+"&value="+$('input.'+typeId+'text').val(),	//后台用 request.getParameter("key");
                        dataType : "json",  //返回数据的 类型 text|json|html--
                        success : function(users){	//回调函数 和 后台返回的 数据



                        }
                    });

                });

            }




            break;

        case "EventConditionStartSetter":

            $("div.Main").append("  <input type='text' class='EventConditionStartSetter' />  ");
            $('input.EventConditionStartSetter').removeClass("EventConditionStartSetter").addClass(typeId+'text');
            $('input.'+typeId+'text').css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w*0.7});



            $("div.Main").append("  <input type='button' class='EventConditionStartSetter' />  ");
            $('input.EventConditionStartSetter').removeClass("EventConditionStartSetter").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+0.71*w,"top":y,"height":h,"width":w*0.29});
            $("input."+typeId+'button').attr('value',user.content);
            $("input."+typeId+'button').attr('color',user.fontColor);
            $("input."+typeId+'button').attr('font-size',user.fontSize);

            if(user.click==true)//如果按钮有点击事件
            {
                $('input.'+typeId+'button').click(function () {


                    var title=$(document).attr('title');


                    $.ajax({
                        url :  "onClick",	//请求url
                        type : "POST",	//请求类型  post|get
                        data : "titleName="+title+"&typeId="+typeId+"&value="+$('input.'+typeId+'text').val(),	//后台用 request.getParameter("key");
                        dataType : "json",  //返回数据的 类型 text|json|html--
                        success : function(users){	//回调函数 和 后台返回的 数据



                        }
                    });

                });

            }




            break;



        case "ChangePassWord":

            //alert("ChangePassWord");
            $("div.Main").append("  <input type='text' class='ChangePassWord' />  ");
            $('input.ChangePassWord').removeClass("ChangePassWord").addClass(typeId+'text');
            $('input.'+typeId+'text').css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w});

            break;

        case "SMSConfig":


            $("div.Main").append(" <font class='SMSConfig'>1</font>  ");
            $("font.SMSConfig").removeClass("SMSConfig").addClass(typeId);
            $("font."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w/10*0.89,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});
            $("font."+typeId).text(user.labelOrder);

            $("div.Main").append("  <input type='text' class='SMSConfig' />  ");
            $('input.SMSConfig').removeClass("SMSConfig").addClass(typeId+'text'+1);
            $('input.'+typeId+'text'+1).css({"position":pos,'z-index':index,"left":x+w/10*0.89,"top":y,"height":h,"width":w*1.9/10*0.89,'color':user.fontColor,'fontSize':user.fontSize});
            $("input."+typeId+'text'+1).attr('placeholder','姓名');

            $("div.Main").append("  <input type='text' class='SMSConfig' />  ");
            $('input.SMSConfig').removeClass("SMSConfig").addClass(typeId+'text'+2);
            $('input.'+typeId+'text'+2).css({"position":pos,'z-index':index,"left":x+w*3/10*0.89,"top":y,"height":h,"width":w*1.9/10*0.89,'color':user.fontColor,'fontSize':user.fontSize});
            $("input."+typeId+'text'+2).attr('placeholder','号码');

            $("div.Main").append("  <input type='text' class='SMSConfig' />  ");
            $('input.SMSConfig').removeClass("SMSConfig").addClass(typeId+'text'+3);
            $('input.'+typeId+'text'+3).css({"position":pos,'z-index':index,"left":x+w*5/10*0.89,"top":y,"height":h,"width":w*1.9/10*0.89,'color':user.fontColor,'fontSize':user.fontSize});
            $("input."+typeId+'text'+3).attr('placeholder','等级');



            $("div.Main").append("  <input type='button' class='SMSConfig' />  ");
            $('input.SMSConfig').removeClass("SMSConfig").addClass(typeId+'button'+1);
            $('input.'+typeId+'button'+1).css({"position":pos,'z-index':index,"left":x+w*7/10*0.89,"top":y,"height":h,"width":w*1.4/10*0.89,'color':user.fontColor,'fontSize':user.fontSize});
            $('input.'+typeId+'button'+1).attr('value','修改');

            $("div.Main").append("  <input type='button' class='SMSConfig' />  ");
            $('input.SMSConfig').removeClass("SMSConfig").addClass(typeId+'button'+2);
            $('input.'+typeId+'button'+2).css({"position":pos,'z-index':index,"left":x+w*8.5/10*0.89,"top":y,"height":h,"width":w*1.4/10*0.89});
            $('input.'+typeId+'button'+2).attr('value','删除');




            if('Delete'==user.value)
            {
                $("input."+typeId+'text'+1).attr('placeholder','Name');
                $("input."+typeId+'text'+2).attr('placeholder','Phone');
                $("input."+typeId+'text'+3).attr('placeholder','Level');
                $('input.'+typeId+'button'+1).attr('value','Alter');
                $('input.'+typeId+'button'+2).attr('value',user.value);
            }


            var le=Object.keys(user.map).length;
            if(le>0)
            {
                for(var x in user.map){

                    if(x=="name")
                    {
                        $("input."+typeId+'text'+1).attr('value',user.map[x]);
                    }
                    if(x=="tel_number")
                    {
                        $("input."+typeId+'text'+2).attr('value',user.map[x]);
                    }
                    if(x=="alarm_level")
                    {
                        $("input."+typeId+'text'+3).attr('value',user.map[x]);
                    }
                }
            }

            $('input.'+typeId+'button'+1).click(function () {

                var title=$(document).attr('title');


                var mapData={};
                mapData['type']="alter";
                mapData['name']=$("input."+typeId+'text'+1).val();
                mapData['tel_number']=$("input."+typeId+'text'+2).val();
                mapData['alarm_level']=$("input."+typeId+'text'+3).val();

                var jsonstr = JSON.stringify(mapData);


                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+jsonstr,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });


            });


            $('input.'+typeId+'button'+2).click(function () {

                var title=$(document).attr('title');
                var mapData={};
                mapData['type']="delete";
                mapData['name']=$("input."+typeId+'text'+1).val();
                mapData['tel_number']=$("input."+typeId+'text'+2).val();
                mapData['alarm_level']="";

                var jsonstr = JSON.stringify(mapData);


                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+jsonstr,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据





                    }
                });




            });
            

            break;


        case "SaveEquipt":



            var titleHeight=h/22;
            var dataValue=new Date();

            $("div.Main").append("  <select class='SaveEquipt'></select>  ");
            $('select.SaveEquipt').removeClass("SaveEquipt").addClass(typeId+'equip');
           // $('select.'+typeId+'equip').css({"position":pos,'z-index':index,"left":x,"top":y-titleHeight,"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor,'text-align':'center','text-align-last':'center'});
            $('select.'+typeId+'equip').css({"position":pos,'z-index':index,"left":x,"top":y-titleHeight,"height":titleHeight,"width":w/6,"color":user.textColor,'background':user.btnColor,'text-align':'center','text-align-last':'center'});

            for(var i=0; i<user.nameList.length; i++){

             $('select.'+typeId+'equip').append("<option class='opt'>123</option>");
             $('option.opt').removeClass("opt").addClass(typeId+'option'+i);
             $('option.'+typeId+'option'+i).text(user.nameList[i]);

            }



            $("div.Main").append("  <div class='calendarWarp' style='' id='date3'></div>");
            $('#date3').css({"position":pos,'z-index':index,"left":x+w*5/24,"top":y-titleHeight,"height":titleHeight,"width":w/6});
            $('#date3').append("  <input type='text' name='date' class='ECalendar' id='ECalendar_case3' value='设置时间'/>  ");
            $('#ECalendar_case3').css({"height":titleHeight,"width":w/6,"color":user.textColor,'background':user.btnColor});

            $("#ECalendar_case3").ECalendar({
                type:"date",
                skin:"#233",
                format:"yyyy-mm-dd",
                offset:[0,2],
                callback:function(v,e)
                {
                    dataValue=getDate($("#ECalendar_case3").val());
                }
            });


            $("#ECalendar_case3").attr('value',getDateStr(dataValue));


            $("div.Main").append("  <input type='button' value='前一天' class='SaveEquipt' />  ");
            $('input.SaveEquipt').removeClass("SaveEquipt").addClass(typeId+'startTime');
           // $('input.'+typeId+'startTime').css({"position":pos,'z-index':index,"left":x+w/5+w/15,"top":y-titleHeight,"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor});

            $('input.'+typeId+'startTime').css({"position":pos,'z-index':index,"left":x+w*10/24,"top":y-titleHeight,"height":titleHeight,"width":w/6,"color":user.textColor,'background':user.btnColor});

            $('input.'+typeId+'startTime').click(function () {


                dataValue.setDate(dataValue.getDate()-1);
                $("#ECalendar_case3").attr('value',getDateStr(dataValue));

            });




            $("div.Main").append("  <input type='button'  value='后一天' class='SaveEquipt' />  ");
            $('input.SaveEquipt').removeClass("SaveEquipt").addClass(typeId+'endTime');
           // $('input.'+typeId+'endTime').css({"position":pos,'z-index':index,"left":x+w*8/15,"top":y-titleHeight,"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor});

            $('input.'+typeId+'endTime').css({"position":pos,'z-index':index,"left":x+w*15/24,"top":y-titleHeight,"height":titleHeight,"width":w/6,"color":user.textColor,'background':user.btnColor});

            $('input.'+typeId+'endTime').click(function () {



                dataValue.setDate(dataValue.getDate()+1);
                $("#ECalendar_case3").attr('value',getDateStr(dataValue));


            });


            $("div.Main").append("  <input type='button' value='获取' class='SaveEquipt' />  ");
            $('input.SaveEquipt').removeClass("SaveEquipt").addClass(typeId+'button');
           // $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*12/15,"top":y-titleHeight,"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor});


            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*20/24,"top":y-titleHeight,"height":titleHeight,"width":w/6,"color":user.textColor,'background':user.btnColor});




            if('Receipt'==user.value)
            {
                $('#ECalendar_case3').attr('value','SetTime');
                $('input.'+typeId+'startTime').attr('value','Previous Day');
                $('input.'+typeId+'endTime').attr('value','Next Day');
                $('input.'+typeId+'button').attr('value','Receipt');

            }



            $('input.'+typeId+'button').click(function () {




                var title=$(document).attr('title');
                var time=getDateStr(dataValue);

                //alert(time);

                $.ajax({
                    url :  "callback",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&equip="+$('select.'+typeId+'equip').val()+"&time="+time,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(data){	//回调函数 和 后台返回的 数据



                        $("table."+typeId).empty();

                        var  l=100;
                        if(data.listData.length<l)
                        {
                            l=data.listData.length;
                        }

                        for(var i=-1;i<l;i++)
                        {
                            $("table."+typeId).append(" <tr class='Tr'></tr>");
                            $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                            if(i%2==0)
                            {
                                if(i==-1)
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                                }else
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.evenRowBackground});
                                    if(user.evenalpha!=0)
                                    {
                                      //  $("tr."+typeId+'Tr'+i).css({"opacity":user.evenalpha/255});
                                    }
                                }

                            }else
                            {

                                if(i==-1)
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                                }else
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.oddRowBackground});
                                    if(user.oddalpha!=0)
                                    {
                                       // $("tr."+typeId+'Tr'+i).css({"opacity":user.oddalpha/255});
                                    }
                                }

                            }

                            for(var j=0;j<7;j++)
                            {
                                // if(i==-1)
                                // {
                                //
                                //     switch (j)
                                //     {
                                //         case 0:
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>设备名称</td>");
                                //             break;
                                //         case 1:
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>信号名称</td>");
                                //             break;
                                //         case 2:
                                //
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>数值</td>");
                                //             break;
                                //         case 3:
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>单位</td>");
                                //             break;
                                //         case 4:
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>数值类型</td>");
                                //             break;
                                //         case 5:
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>告警等级</td>");
                                //             break;
                                //         case 6:
                                //             $("tr."+typeId+'Tr'+i).append("<td class='Td'>采集时间</td>");
                                //             break;
                                //
                                //
                                //     }
                                // }else
                                // {

                                    $("tr."+typeId+'Tr'+i).append("<td class='Td'>data.listData[i][j]</td>");

                                //}

                                var caa=typeId+'Td'+i+''+j;
                                $("td.Td").removeClass("Td").addClass(caa);
                                $("td."+caa).css({"width":user.wight/user.fromWight*window.screen.availWidth/7});
                                $("td."+caa).css({"text-align":'center'});
                                if(i!=-1)
                                {
                                    $("td."+caa).html(data.listData[i][j]);
                                }else{


                                        $("td."+caa).html(user.lstTitles[j]);


                                }



                            }
                        }


                    }
                });

            });




            $("div.Main").append(" <div class='SaveEquipt'></div>");
            $('div.SaveEquipt').removeClass("SaveEquipt").addClass(typeId);
            $('div.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w,"overflow-y": "scroll"});

            $("div."+typeId).append(" <table class='SignalList' > </table> ");
            $("table.SignalList").removeClass("SignalList").addClass(typeId);
            $("table."+typeId).attr("cellspacing","1");
            $("table."+typeId).attr("align","center");





            break;

        case "HisEvent":



            var titleHeight=h/22;

            $("div.Main").append("  <select class='SaveEquipt'></select>  ");
            $('select.SaveEquipt').removeClass("SaveEquipt").addClass(typeId+'equip');
            $('select.'+typeId+'equip').css({"position":pos,'z-index':index,"left":x,"top":y-titleHeight,"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor,'text-align':'center','text-align-last':'center'});

            for(var i=0; i<user.nameList.length; i++){

                $('select.'+typeId+'equip').append("<option class='opt'>123</option>");
                $('option.opt').removeClass("opt").addClass(typeId+'option'+i);
                $('option.'+typeId+'option'+i).text(user.nameList[i]);
            }

      

            $("div.Main").append("  <div class='calendarWarp' style='' id='date1'></div>");
            $('#date1').css({"position":pos,'z-index':index,"left":x+w/5+w/15,"top":y-titleHeight,"height":titleHeight,"width":w/5});
            $('#date1').append("  <input type='text' name='date' class='ECalendar' id='ECalendar_case1' value='开始时间'/>  ");
            $('#ECalendar_case1').css({"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor});

            $("#ECalendar_case1").ECalendar({
                type:"date",
                skin:"#233",
                format:"yyyy-mm-dd",
                offset:[0,2]
            });





            $("div.Main").append("  <div class='calendarWarp' style='' id='date2'></div>");
            $('#date2').css({"position":pos,'z-index':index,"left":x+w*8/15,"top":y-titleHeight,"height":titleHeight,"width":w/5});
            $('#date2').append("  <input type='text' name='date' class='ECalendar' id='ECalendar_case2' value='结束时间'/>  ");
            $('#ECalendar_case2').css({"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor});

            $("#ECalendar_case2").ECalendar({
                type:"date",
                skin:"#233",
                format:"yyyy-mm-dd",
                offset:[0,2]
            });




            $("div.Main").append("  <input type='button' value='获取' class='SaveEquipt' />  ");
            $('input.SaveEquipt').removeClass("SaveEquipt").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*12/15,"top":y-titleHeight,"height":titleHeight,"width":w/5,"color":user.textColor,'background':user.btnColor});



            if('Receipt'==user.value)
            {
                $('#ECalendar_case1').attr('value','Start Time');
                $('#ECalendar_case2').attr('value','End Time');
                $('input.'+typeId+'button').attr('value','Receipt');


            }


            $('input.'+typeId+'button').click(function () {

                var title=$(document).attr('title');
               // alert("titleName="+title+"&typeId="+typeId+"&equip="+$('select.'+typeId+'equip').val()+"&startTime="+$('input.'+typeId+'startTime').val()+"&endTime="+ $('input.'+typeId+'endTime').val());


                $.ajax({
                    url :  "callback",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&equip="+$('select.'+typeId+'equip').val()+"&startTime="+ $('#ECalendar_case1').val()+"&endTime="+ $('#ECalendar_case2').val(),	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(data){	//回调函数 和 后台返回的 数据


                        $("table."+typeId).empty();

                        var  l=1000;
                        if(data.listData.length<l)
                        {
                            l=data.listData.length;
                        }

                        for(var i=-1;i<l;i++)
                        {
                            $("table."+typeId).append(" <tr class='Tr'></tr>");
                            $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                            if(i%2==0)
                            {
                                if(i==-1)
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                                }else
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.evenRowBackground});

                                }

                            }else
                            {

                                if(i==-1)
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                                }else
                                {
                                    $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.oddRowBackground});

                                }

                            }

                            for(var j=0;j<data.lstTitles.length;j++)
                            {
                          

                                $("tr."+typeId+'Tr'+i).append("<td class='Td'>data.listData[i][j]</td>");
                                var caa=typeId+'Td'+i+''+j;
                                $("td.Td").removeClass("Td").addClass(caa);
                                $("td."+caa).css({"width":user.wight/user.fromWight*window.screen.availWidth/data.lstTitles.length});
                                $("td."+caa).css({"text-align":'center'});
                                if(i!=-1)
                                {
                                    $("td."+caa).html(data.listData[i][j]);
                                }else
                                {
                                    $("td."+caa).html(data.lstTitles[j]);
                                }



                            }
                        }






                    }
                });

            });





            $("div.Main").append(" <div class='SaveEquipt'></div>");
            $('div.SaveEquipt').removeClass("SaveEquipt").addClass(typeId);
            $('div.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w,"overflow-y": "scroll"});

            $("div."+typeId).append(" <table class='SignalList' > </table> ");
            $("table.SignalList").removeClass("SignalList").addClass(typeId);
            $("table."+typeId).attr("cellspacing","1");
            $("table."+typeId).attr("align","center");


            break;

        case "Form":




            if(user.image!=undefined)
            {

                $("div.Main").append(" <img  class='Label'/>  ");
                $('img.Label').removeClass("Label").addClass("Form");
                $('img.Form').css({"position":pos,'z-index':index,"left":x,"top":y,"alt":'fali',"height":h,"width":w});
                $('img.Form').attr("src",user.image);

            }else
            {
                $("div.Main").css({"background":user.bg});
            }
            break;


        case "SgHalfCircleChar":



            $("div.main").append("<div class='SgHalfCircleChar'></div>")
            $("div.SgHalfCircleChar").removeClass("SgHalfCircleChar").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y-h/10,"height":h,"width":w})
            $("div."+typeId).attr('id',typeId);

            setGrdata2(typeId,"",user.minValue,user.maxValue,user.value,user.listValue,user.listColor);

            break;


        case "SgClickPieChart":




            $("div.main").append("<div class='SgClickPieChart'></div>")
            $("div.SgClickPieChart").removeClass("SgClickPieChart").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w})
            $("div."+typeId).attr('id',typeId);

            setPiedata(typeId,user);

            break;

        case "Dial":





            $("div.main").append("<div class='Dial'></div>")
            $("div.Dial").removeClass("Dial").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x-((1.3-1)*w)/2,"top":y-((1.3-1)*h)/2,"height":h*1.3,"width":w*1.3});
            $("div."+typeId).attr('id',typeId);

            setCriData(typeId,user);

            break;

        case "SgSplineChart":


          

            $("div.main").append("<div class='SgSplineChart'></div>")
            $("div.SgSplineChart").removeClass("SgSplineChart").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x-((1.1-1)*w)/2,"top":y-((1.2-1)*h)/2,"height":h*1.2,"width":w*1.1});
            $("div."+typeId).attr('id',typeId);


            $("div.main").append("<input type='radio' class='AutoSigList' checked='checked' value='时' /><font class='AutoSigList'>时</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"h");
            $("input."+typeId+"h").attr("name",typeId);
            $("input."+typeId+"h").css({"position":pos,'z-index':index,"left":x,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"h");
            $("font."+typeId+"h").css({"position":pos,'z-index':index,"left":x+w/8+15,"top":y,"height":10,"width":10,"color":user.fontColor});




            $("input."+typeId+"h").click(function () {


                map[typeId] = $("input."+typeId+"h").val();

                setLineChart(typeId,user,map[typeId]);


            });

            $("div.main").append("<input type='radio' class='AutoSigList' value='日'/><font class='AutoSigList'>日</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"d");
            $("input."+typeId+"d").attr("name",typeId);
            $("input."+typeId+"d").css({"position":pos,'z-index':index,"left":x+w/4,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"d");
            $("font."+typeId+"d").css({"position":pos,'z-index':index,"left":x+w*3/8+15,"top":y,"height":10,"width":10,"color":user.fontColor});

            $("input."+typeId+"d").click(function () {


                map[typeId] = $("input."+typeId+"d").val();

                setLineChart(typeId,user,map[typeId]);

            });

            $("div.main").append("<input type='radio'  class='AutoSigList' value='月'/><font class='AutoSigList'>月</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"m");
            $("input."+typeId+"m").attr("name",typeId);
            $("input."+typeId+"m").css({"position":pos,'z-index':index,"left":x+w/2,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"m");
            $("font."+typeId+"m").css({"position":pos,'z-index':index,"left":x+w*5/8+15,"top":y,"height":10,"width":10,"color":user.fontColor});

            $("input."+typeId+"m").click(function () {

                map[typeId] = $("input."+typeId+"m").val();

                setLineChart(typeId,user,map[typeId]);

            });

            $("div.main").append("<input type='radio' class='AutoSigList' value='年'/><font class='AutoSigList'>年</font>");
            $("input.AutoSigList").removeClass("AutoSigList").addClass(typeId+"y");
            $("input."+typeId+"y").attr("name",typeId);
            $("input."+typeId+"y").css({"position":pos,'z-index':index,"left":x+w*3/4,"top":y,"height":17,"width":w/4});
            $("font.AutoSigList").removeClass("AutoSigList").addClass(typeId+"y");
            $("font."+typeId+"y").css({"position":pos,'z-index':index,"left":x+w*7/8+15,"top":y,"height":10,"width":10,"color":user.fontColor});

            $("input."+typeId+"y").click(function () {

                map[typeId] = $("input."+typeId+"y").val();
                setLineChart(typeId,user,map[typeId]);
            });

         
                $("font."+typeId+"h").text(user.h);
                $("font."+typeId+"d").text(user.d);
                $("font."+typeId+"m").text(user.m);
                $("font."+typeId+"y").text(user.y);
            

            map[typeId] ="时";
            setLineChart(typeId,user, map[typeId]);

            break;


        case "SgBarChartView":



            $("div.Main").append("<div  class='SgBarChartView'></div> ");
            $("div.SgBarChartView").removeClass("SgBarChartView").addClass(typeId);
            $("div."+typeId).attr('id',typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w});


            if(user.math)
            {


                $("div.main").append("<input type='radio' class='SgBarChartView'  value='year' /><font class='SgBarChartView'>year</font>");
                $("input.SgBarChartView").removeClass("SgBarChartView").addClass(typeId+"year");
                $("input."+typeId+"year").attr("name",typeId);
                $("input."+typeId+"year").css({"position":pos,'z-index':index,"left":x,"top":y,"height":17,"width":w/3});
                $("font.SgBarChartView").removeClass("SgBarChartView").addClass(typeId+"year");
                $("font."+typeId+"year").css({"position":pos,'z-index':index,"left":x+w/6+15,"top":y,"height":10,"width":10,"color":user.fontColor});

                $("input."+typeId+"year").click(function () {

                    sgBarMap[typeId]='3';
                    setNewBardata(typeId,"电能",user,3);


                });



                $("div.main").append("<input type='radio' class='SgBarChartView' value='mon'/><font class='SgBarChartView'>mon</font>");
                $("input.SgBarChartView").removeClass("SgBarChartView").addClass(typeId+"mon");
                $("input."+typeId+"mon").attr("name",typeId);
                $("input."+typeId+"mon").css({"position":pos,'z-index':index,"left":x+w/3,"top":y,"height":17,"width":w/3});
                $("font.SgBarChartView").removeClass("SgBarChartView").addClass(typeId+"mon");
                $("font."+typeId+"mon").css({"position":pos,'z-index':index,"left":x+w/3+w/6+15,"top":y,"height":10,"width":10,"color":user.fontColor});

                $("input."+typeId+"mon").click(function () {

                    sgBarMap[typeId]='2';
                    setNewBardata(typeId,"电能",user,2);

                });

                $("div.main").append("<input type='radio'  class='SgBarChartView'  checked='checked' value='day'/><font class='SgBarChartView'>day</font>");
                $("input.SgBarChartView").removeClass("SgBarChartView").addClass(typeId+"day");
                $("input."+typeId+"day").attr("name",typeId);
                $("input."+typeId+"day").css({"position":pos,'z-index':index,"left":x+w*2/3,"top":y,"height":17,"width":w/3});
                $("font.SgBarChartView").removeClass("SgBarChartView").addClass(typeId+"day");
                $("font."+typeId+"day").css({"position":pos,'z-index':index,"left":x+w*2/3+w/6+15,"top":y,"height":10,"width":10,"color":user.fontColor});

                $("input."+typeId+"day").click(function () {

                    sgBarMap[typeId]='1';
                    setNewBardata(typeId,"电能",user,1);

                });

                sgBarMap[typeId]='1';
                setNewBardata(typeId,"电能",user,1);

            }else
            {
                setOldBardata(typeId,"温度",user);
            }





            break;


        case "TextClock":


            $("div.Main").append("  <font  class='TextClock'></font>  ");
            $('font.TextClock').removeClass("TextClock").addClass(typeId);
            $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w,'text-align':'center','line-height':h+'px',"font-size":user.textSize,'color':user.textColor});
            displayTime(user);

            break;

        case "StatePanel":


            $("div.Main").append("  <img  class='StatePanel' alt='fail'/>  ");
            $('img.StatePanel').removeClass("StatePanel").addClass(typeId);
            $('img.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"alt":'fali',"height":h,"width":w});
            if(user.value==0)
            {
                $('img.'+typeId).attr("src",'image/normal.png');

            }else if(user.value==1)
            {
                $('img.'+typeId).attr("src",'image/error.png');
            }else if(user.value==2)
            {
                $('img.'+typeId).attr("src",'image/warning.png');
            }

            break;


        case "RC_Label":



            var title=$(document).attr('title');

            $("div.Main").append("<div  class='RC_Label'></div> ");
            $("div.RC_Label").removeClass("RC_Label").addClass(typeId);
            $("div."+typeId).attr('id',typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w});




            $("div.main").append("<input type='radio' class='RC_Label'  value='year' /><font class='RC_Label'>year</font>");
            $("input.RC_Label").removeClass("RC_Label").addClass(typeId+"year");
            $("input."+typeId+"year").attr("name",typeId);
            $("input."+typeId+"year").css({"position":pos,'z-index':index,"left":x,"top":y,"height":17,"width":w/3});
            $("font.RC_Label").removeClass("RC_Label").addClass(typeId+"year");
            $("font."+typeId+"year").css({"position":pos,'z-index':index,"left":x+w/6+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"year").click(function () {



                $.ajax({
                    url :  "callback",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+$("input."+typeId+"year").val(),	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(data){	//回调函数 和 后台返回的 数据

                        setBardata(typeId,"",user,3,data);

                    }
                });

            });



            $("div.main").append("<input type='radio' class='RC_Label' value='mon'/><font class='RC_Label'>mon</font>");
            $("input.RC_Label").removeClass("RC_Label").addClass(typeId+"mon");
            $("input."+typeId+"mon").attr("name",typeId);
            $("input."+typeId+"mon").css({"position":pos,'z-index':index,"left":x+w/3,"top":y,"height":17,"width":w/3});
            $("font.RC_Label").removeClass("RC_Label").addClass(typeId+"mon");
            $("font."+typeId+"mon").css({"position":pos,'z-index':index,"left":x+w/3+w/6+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"mon").click(function () {


                $.ajax({
                    url :  "callback",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+$("input."+typeId+"mon").val(),	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(data){	//回调函数 和 后台返回的 数据


                        setBardata(typeId,"",user,2,data);

                    }
                });

            });

            $("div.main").append("<input type='radio'  class='RC_Label'  checked='checked' value='day'/><font class='RC_Label'>day</font>");
            $("input.RC_Label").removeClass("RC_Label").addClass(typeId+"day");
            $("input."+typeId+"day").attr("name",typeId);
            $("input."+typeId+"day").css({"position":pos,'z-index':index,"left":x+w*2/3,"top":y,"height":17,"width":w/3});
            $("font.RC_Label").removeClass("RC_Label").addClass(typeId+"day");
            $("font."+typeId+"day").css({"position":pos,'z-index':index,"left":x+w*2/3+w/6+15,"top":y,"height":10,"width":10});

            $("input."+typeId+"day").click(function () {

                $.ajax({
                    url :  "callback",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+$("input."+typeId+"day").val(),	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(data){	//回调函数 和 后台返回的 数据


                        setBardata(typeId,"",user,1,data);

                    }
                });

            });



            $.ajax({
                url :  "callback",	//请求url
                type : "POST",	//请求类型  post|get
                data : "titleName="+title+"&typeId="+typeId+"&value="+$("input."+typeId+"day").val(),	//后台用 request.getParameter("key");
                dataType : "json",  //返回数据的 类型 text|json|html--
                success : function(data){	//回调函数 和 后台返回的 数据

                    setBardata(typeId,"",user,1,data);

                }
            });



            break;

        case "ELabel":




            $("div.Main").append("  <font  class='ELabel'></font>  ");
            $('font.ELabel').removeClass("ELabel").addClass(typeId);


            $('font.'+typeId).text(user.text);


            $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":user.textSize,"height":h,"width":w,'text-align':'center','color':user.textColor,'line-height':h+'px'});


            break;

        case "AlarmCount":





            $("div.Main").append("  <font  class='AlarmCount'></font>  ");
            $('font.AlarmCount').removeClass("AlarmCount").addClass(typeId);


            $('font.'+typeId).text(user.text);


            $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":'15',"height":5/6*h,"width":4/6*w,'text-align':'center','color':'#ffffff','line-height':5/6*h+'px'});
            if(user.grad==1)
            {
                $('font.'+typeId).css({'background':'#65AADC'});
            }
            else if(user.grad==2)
           {
            $('font.'+typeId).css({'background':'#F7CC4A'});
           }
            else if(user.grad==3)
           {
            $('font.'+typeId).css({'background':'#f65a48'});
           }
           else
          {
            $('font.'+typeId).css({'background':'#ff0000'});
          }


            break;


        case "ChangXmlPW":



            $("div.Main").append(" <font class='ChangXmlPW'>旧密码：</font>  ");
            $("font.ChangXmlPW").removeClass("ChangXmlPW").addClass(typeId+"1");
            $("font."+typeId+"1").css({"position":pos,'z-index':index,"left":x+w/10,"top":y+h/10,"height":h*0.14,"width":w/5,'text-align':'center','line-height':h*0.14+'px','background':'transparent','fontSize':'20','color':user.fontColor});


            $("div.Main").append("  <input type='text' class='ChangXmlPW' />  ");
            $('input.ChangXmlPW').removeClass("ChangXmlPW").addClass(typeId+'text'+1);
            $('input.'+typeId+'text'+1).css({"position":pos,'z-index':index,"left":x+w* 0.35,"top":y+h/10,"height":h*0.14,"width":w*0.55,'color':'Red','fontSize':'20'});


            $("div.Main").append(" <font class='ChangXmlPW'>新密码：</font>  ");
            $("font.ChangXmlPW").removeClass("ChangXmlPW").addClass(typeId+"2");
            $("font."+typeId+"2").css({"position":pos,'z-index':index,"left":x+w/10,"top":y+h*0.34,"height":h*0.14,"width":w/5,'text-align':'center','line-height':h*0.14+'px','background':'transparent','fontSize':'20','color':user.fontColor});


            $("div.Main").append("  <input type='text' class='ChangXmlPW' />  ");
            $('input.ChangXmlPW').removeClass("ChangXmlPW").addClass(typeId+'text'+2);
            $('input.'+typeId+'text'+2).css({"position":pos,'z-index':index,"left":x+w* 0.35,"top":y+h*0.34,"height":h*0.14,"width":w*0.55,'color':'Red','fontSize':'20'});


            $("div.Main").append(" <font class='ChangXmlPW'>确 认：</font>  ");
            $("font.ChangXmlPW").removeClass("ChangXmlPW").addClass(typeId+"3");
            $("font."+typeId+"3").css({"position":pos,'z-index':index,"left":x+w/10,"top":y+h*0.58,"height":h*0.14,"width":w/5,'text-align':'center','line-height':h*0.14+'px','background':'transparent','fontSize':'20','color':user.fontColor});


            $("div.Main").append("  <input type='text' class='ChangXmlPW' />  ");
            $('input.ChangXmlPW').removeClass("ChangXmlPW").addClass(typeId+'text'+3);
            $('input.'+typeId+'text'+3).css({"position":pos,'z-index':index,"left":x+w* 0.35,"top":y+h*0.58,"height":h*0.14,"width":w*0.55,'color':'Red','fontSize':'20'});



            $("div.Main").append("  <input type='button' value='修改' class='ChangXmlPW' />  ");
            $('input.ChangXmlPW').removeClass("ChangXmlPW").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*0.42,"top":y+0.82*h,"height":h*0.18,"width":w*0.23,"color":"Black"});


			
			
           
                $("font."+typeId+"1").text(user.oldPw);
                $("font."+typeId+"2").text(user.newPw);
                $("font."+typeId+"3").text(user.ok);
                $('input.'+typeId+'button').val(user.alter);
            




            $('input.'+typeId+'button').click(function () {


                var title=$(document).attr('title');


                var value=  $('input.'+typeId+'text'+1).val()+"-"+$('input.'+typeId+'text'+2).val()+"-"+$('input.'+typeId+'text'+3).val();
                //(value);

                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+value,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });

            });



            break;

        case "ChangExpression":




            $("div.Main").append("  <input type='text' class='ChangExpression' />  ");
            $('input.ChangExpression').removeClass("ChangExpression").addClass(typeId+'text');
            $('input.'+typeId+'text').css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w*0.64,'color':'Red','fontSize':'20'});

            $("div.Main").append("  <input type='button' value='设置' class='ChangExpression' />  ");
            $('input.ChangExpression').removeClass("ChangExpression").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*0.65,"top":y,"height":h,"width":w*0.35,"color":"Black"});
            $('input.'+typeId+'button').val(user.value);


            $('input.'+typeId+'button').click(function () {


                var title=$(document).attr('title');


                //alert(title+":"+typeId+":"+$('input.'+typeId+'text').val());

                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+$('input.'+typeId+'text').val(),	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });

            });





            break;

        case "SgAlarmActionShow":




            $("div.Main").append("  <font  class='SgAlarmActionShow'></font>  ");
            $('font.SgAlarmActionShow').removeClass("SgAlarmActionShow").addClass(typeId);

            $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":user.textSize,"height":h,"width":w,'text-align':'center','color':user.textColor,'line-height':h+'px'});

            $('font.'+typeId).text(user.text);


            break;

        case "SgAlarmChangTime":




            $("div.Main").append("  <input type='text' class='SgAlarmChangTime' />  ");
            $('input.SgAlarmChangTime').removeClass("SgAlarmChangTime").addClass(typeId+'text');
            $('input.'+typeId+'text').css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w*0.64,'color':'Red','fontSize':'20'});

            $("div.Main").append("  <input type='button' value='设置' class='SgAlarmChangTime' />  ");
            $('input.SgAlarmChangTime').removeClass("SgAlarmChangTime").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*0.65,"top":y,"height":h,"width":w*0.35,"color":"Black"});






            break;


        case "AlarmLevel":




            $("div.Main").append(" <div   class='AlarmLevel' > <div/> ");
            $("div.AlarmLevel").removeClass("AlarmLevel").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w,"overflow-y": "scroll","background-color":'#ffffff'});
            $("div."+typeId).append(" <table class='AlarmLevel' > </table> ");
            $("table.AlarmLevel").removeClass("AlarmLevel").addClass(typeId);
            $("table."+typeId).attr("cellspacing","1");
            $("table."+typeId).attr("align","center");


            for(var i=0;i<user.list.length;i++)
            {

                $("table."+typeId).append(" <tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                $("tr."+typeId+'Tr'+i).css({"color":'#00ffff',"background":user.lineColor});

                $("tr."+typeId+'Tr'+i).append("<td class='Td'></td>");
                $("td.Td").removeClass("Td").addClass(typeId+'Td'+i);
                $("td."+typeId+'Td'+i).css({"width":user.wight/user.fromWight*window.screen.availWidth/6,"text-align":'center'});
                $("td."+typeId+'Td'+i).append("<img  class='AlarmLevel' alt='fail'/>");

                $("img.AlarmLevel").removeClass("AlarmLevel").addClass(typeId+i);


                if(user.list[i].img==2130837518)
                {
                    $('img.'+typeId+i).attr("src",'image/hk.png');

                }else if(user.list[i].img==2130837516)
                {
                    $('img.'+typeId+i).attr("src",'image/hi.png');

                }else if(user.list[i].img==2130837517)
                {
                    $('img.'+typeId+i).attr("src",'image/hj.png');
                }




                $("tr."+typeId+'Tr'+i).append("<tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tro'+i);

                $("tr."+typeId+'Tro'+i).css({"color":user.titleColor,"background":user.lineColor});

                $("tr."+typeId+'Tro'+i).append("<td class='Td'>2018.11.06 11:33:05</td>");
                $("td.Td").removeClass("Td").addClass(typeId+'Tdo'+i);
                $("td."+typeId+'Tdo'+i).css({"width":user.wight/user.fromWight*window.screen.availWidth*5/6});
                $("td."+typeId+'Tdo'+i).html(user.list[i].time);


                $("tr."+typeId+'Tr'+i).append("<tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Trt'+i);

                $("tr."+typeId+'Trt'+i).css({"color":user.infoColor,"background":user.lineColor});

                $("tr."+typeId+'Trt'+i).append("<td class='Td'>温湿度-COM2--设备通讯状态:中断 等级:严重告警</td>");
                $("td.Td").removeClass("Td").addClass(typeId+'Tdt'+i);
                $("td."+typeId+'Tdt'+i).css({"width":user.wight/user.fromWight*window.screen.availWidth*5/6});
                $("td."+typeId+'Tdt'+i).html(user.list[i].value);


            }



            break;

        case "DoorInvented":


            $("div.Main").append(" <div   class='DoorInvented' > <div/> ");
            $("div.DoorInvented").removeClass("DoorInvented").addClass(typeId);
            $('div.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"background-color":"transparent","height":h,"width":w,'border':'solid 1px #000000'});


            $("div.Main").append("  <input type='text' class='DoorInvented' />");
            $("input.DoorInvented").removeClass("DoorInvented").addClass(typeId);
            $('input.'+typeId).css({"position":pos,'z-index':index,"left":x+0.1*w,"top":y+0.05*h,"height":0.14*h,"width":0.8*w,'color':'black','fontSize':'20'});


            for(var i=1;i<=3;i++)
            {
                $("div.Main").append("  <input type='button' class='DoorInvented' />");
                $("input.DoorInvented").removeClass("DoorInvented").addClass(typeId+i);
                $('input.'+typeId+i).css({"position":pos,'z-index':index,"left":x+(0.1 + (i - 1) * 0.3)*w,"top":y+0.24 *h,"height":0.14*h,"width":0.2*w,'color':'black','fontSize':'20'});
                $('input.'+typeId+i).val(i);
            }

            for(var i=4;i<=6;i++)
            {
                $("div.Main").append("  <input type='button' class='DoorInvented' />");
                $("input.DoorInvented").removeClass("DoorInvented").addClass(typeId+i);
                $('input.'+typeId+i).css({"position":pos,'z-index':index,"left":x+(0.1 + (i - 1 - 3) * 0.3)*w,"top":y+ 0.43 *h,"height":0.14*h,"width":0.2*w,'color':'black','fontSize':'20'});
                $('input.'+typeId+i).val(i);
            }

            for(var i=7;i<=9;i++)
            {
                $("div.Main").append("  <input type='button' class='DoorInvented' />");
                $("input.DoorInvented").removeClass("DoorInvented").addClass(typeId+i);
                $('input.'+typeId+i).css({"position":pos,'z-index':index,"left":x+(0.1 + (i - 1 - 3 - 3) * 0.3)*w,"top":y+0.62 *h,"height":0.14*h,"width":0.2*w,'color':'black','fontSize':'20'});
                $('input.'+typeId+i).val(i);
            }

            for(var i=10;i<=12;i++)
            {
                $("div.Main").append("  <input type='button' class='DoorInvented' />");
                $("input.DoorInvented").removeClass("DoorInvented").addClass(typeId+i);
                if(i==10)
                {
                    $('input.'+typeId+i).css({"position":pos,'z-index':index,"left":x+0.1*w,"top":y+0.81 *h,"height":0.14*h,"width":0.2*w,'color':'black','fontSize':'20'});
                    $('input.'+typeId+i).val("清空");

                }else if(i==11)
                {

                    $('input.'+typeId+i).css({"position":pos,'z-index':index,"left":x+0.4*w,"top":y+0.81 *h,"height":0.14*h,"width":0.2*w,'color':'black','fontSize':'20'});
                    $('input.'+typeId+i).val("0");

                }else if(i==12)
                {

                    $('input.'+typeId+i).css({"position":pos,'z-index':index,"left":x+0.7*w,"top":y+0.81 *h,"height":0.14*h,"width":0.2*w,'color':'black','fontSize':'20'});
                    $('input.'+typeId+i).val("确认");

                }

            }

            $('input.'+typeId+12).click(function () {



                var title=$(document).attr('title');

                var value=$('input.'+typeId).val();


                if(getCookie('user')!="")
                {

                        values=getCookie('user')+"-"+value;

                         //alert(values);

                        $.ajax({
                            url :  "onClick",	//请求url
                            type : "POST",	//请求类型  post|get
                            data : "titleName="+title+"&typeId="+typeId+"&value="+values,	//后台用 request.getParameter("key");
                            dataType : "json",  //返回数据的 类型 text|json|html--
                            success : function(users){	//回调函数 和 后台返回的 数据



                            }
                        });

                }else
                {

                    alert("没有用户名");

                }






            });







            break;

        case "ChangeUserInfo":



            $("div.Main").append(" <font class='ChangeUserInfo'>1</font>  ");
            $("font.ChangeUserInfo").removeClass("ChangeUserInfo").addClass(typeId);
            $("font."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});
            $("font."+typeId).text(user.index);

            $("div.Main").append("  <input type='text' class='ChangeUserInfo' />  ");
            $('input.ChangeUserInfo').removeClass("ChangeUserInfo").addClass(typeId+'text'+1);
            $('input.'+typeId+'text'+1).css({"position":pos,'z-index':index,"left":x+w/10,"top":y,"height":h,"width":w*1.9/10,'color':"Red",'fontSize':'20'});
            $("input."+typeId+'text'+1).attr('placeholder','用户ID');

            $("div.Main").append("  <input type='text' class='ChangeUserInfo' />  ");
            $('input.ChangeUserInfo').removeClass("ChangeUserInfo").addClass(typeId+'text'+2);
            $('input.'+typeId+'text'+2).css({"position":pos,'z-index':index,"left":x+w*3/10,"top":y,"height":h,"width":w*1.9/10,'color':"Red",'fontSize':'20'});
            $("input."+typeId+'text'+2).attr('placeholder','用户密码');

            $("div.Main").append("  <input type='text' class='ChangeUserInfo' />  ");
            $('input.ChangeUserInfo').removeClass("ChangeUserInfo").addClass(typeId+'text'+3);
            $('input.'+typeId+'text'+3).css({"position":pos,'z-index':index,"left":x+w*5/10,"top":y,"height":h,"width":w*1.9/10,'color':"Red",'fontSize':'20'});
            $("input."+typeId+'text'+3).attr('placeholder','有效时间');



            $("div.Main").append("  <input type='button' class='ChangeUserInfo' />  ");
            $('input.ChangeUserInfo').removeClass("ChangeUserInfo").addClass(typeId+'button'+1);
            $('input.'+typeId+'button'+1).css({"position":pos,'z-index':index,"left":x+w*7/10,"top":y,"height":h,"width":w*1.4/10,"fontSize":'20'});
            $('input.'+typeId+'button'+1).attr('value','修改');

            $("div.Main").append("  <input type='button' class='ChangeUserInfo' />  ");
            $('input.ChangeUserInfo').removeClass("ChangeUserInfo").addClass(typeId+'button'+2);
            $('input.'+typeId+'button'+2).css({"position":pos,'z-index':index,"left":x+w*8.5/10,"top":y,"height":h,"width":w*1.4/10,"fontSize":'20'});
            $('input.'+typeId+'button'+2).attr('value','删除');


            var le=Object.keys(user.mapData).length;
            if(le>0)
            {
                for(var x in user.mapData){



                    if(x=="uid")
                    {

                        $("input."+typeId+'text'+1).attr('value',user.mapData[x]);
                    }
                    if(x=="pw")
                    {
                        $("input."+typeId+'text'+2).attr('value',user.mapData[x]);
                    }
                    if(x=="time")
                    {
                        $("input."+typeId+'text'+3).attr('value',user.mapData[x]);
                    }
                }
            }

            $('input.'+typeId+'button'+1).click(function () {

                var title=$(document).attr('title');


                var mapData={};
                mapData['type']="alter";
                mapData['uid']=$("input."+typeId+'text'+1).val();
                mapData['pw']=$("input."+typeId+'text'+2).val();
                mapData['time']=$("input."+typeId+'text'+3).val();

                var jsonstr = JSON.stringify(mapData);



                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+jsonstr,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });


            });

            $('input.'+typeId+'button'+2).click(function () {

                var title=$(document).attr('title');


                var mapData={};
                mapData['type']="delete";
                mapData['uid']=$("input."+typeId+'text'+1).val();
                mapData['pw']=$("input."+typeId+'text'+2).val();
                mapData['time']=$("input."+typeId+'text'+3).val();

                var jsonstr = JSON.stringify(mapData);



                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+jsonstr,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });


            });


            break;


        case "StateButton":

            $("div.Main").append(" <img  class='StateButton' alt='fail'/>  ");
            $('img.StateButton').removeClass("StateButton").addClass(typeId);
            $('img.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"alt":'fali',"height":h,"width":w});
            $('img.'+typeId).attr("src",user.imagePath);

            $('img.'+typeId).click(function () {



                var title=$(document).attr('title');

                //alert(title);

                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });

            });


            break;

        case "StartAndEndTriggerSet":



            $("div.Main").append(" <font class='StartAndEndTriggerSet'>开始：</font>  ");
            $("font.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"1");
            $("font."+typeId+"1").css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});
            //$("font."+typeId).text(user.labelOrder);

            $("div.Main").append(" <font class='StartAndEndTriggerSet'>0</font>  ");
            $("font.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"2");
            $("font."+typeId+"2").css({"position":pos,'z-index':index,"left":x+w/10,"top":y,"height":h,"width":w/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});

            $("div.Main").append(" <input type='text' class='StartAndEndTriggerSet' />   ");
            $("input.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"3");
            $("input."+typeId+"3").css({"position":pos,'z-index':index,"left":x+w*2/10,"top":y,"height":h,"width":w*2/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});


            $("div.Main").append(" <font class='StartAndEndTriggerSet'>结束：</font>  ");
            $("font.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"4");
            $("font."+typeId+"4").css({"position":pos,'z-index':index,"left":x+w*4/10,"top":y,"height":h,"width":w/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});
            //$("font."+typeId).text(user.labelOrder);

            $("div.Main").append(" <font class='StartAndEndTriggerSet'>0</font>  ");
            $("font.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"5");
            $("font."+typeId+"5").css({"position":pos,'z-index':index,"left":x+w*5/10,"top":y,"height":h,"width":w/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});

            $("div.Main").append(" <input type='text' class='StartAndEndTriggerSet' />   ");
            $("input.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"6");
            $("input."+typeId+"6").css({"position":pos,'z-index':index,"left":x+w*6/10,"top":y,"height":h,"width":w*2/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});

            $("div.Main").append(" <input type='button' class='StartAndEndTriggerSet' value='设置' />   ");
            $("input.StartAndEndTriggerSet").removeClass("StartAndEndTriggerSet").addClass(typeId+"7");
            $("input."+typeId+"7").css({"position":pos,'z-index':index,"left":x+w*8/10+5,"top":y,"height":h,"width":w*2/10,'text-align':'center','line-height':h+'px','background':'transparent','fontSize':'20'});


            if(user.value=="Start:")
            {

                $("font."+typeId+"1").text("Start:");
                $("font."+typeId+"4").text("End:");
            }


            $("font."+typeId+"2").text(user.startValue);
            $("font."+typeId+"5").text(user.stopValue);



            $("input."+typeId+"7").click(function () {


                var title=$(document).attr('title');




                var value=$('input.'+typeId+'3').val()+"-"+$('input.'+typeId+'6').val()

                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+value,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });

            });




            break;

        case "Breaker":




            $("div.Main").append(" <canvas  class='Breaker' width='50px' height='50px'></canvas>");
            $("canvas.Breaker").removeClass("Breaker").addClass(typeId);
            $("canvas."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y});
            $("canvas."+typeId).attr('id',typeId);


            
           setCri(user,typeId,x,y,w,h,1);

            break;


        case "IsolationSwitch":




            $("div.Main").append(" <canvas  class='IsolationSwitch' width='50px' height='50px'></canvas>");
            $("canvas.IsolationSwitch").removeClass("IsolationSwitch").addClass(typeId);
            $("canvas."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y});
            $("canvas."+typeId).attr('id',typeId);


            setCri(user,typeId,x,y,w,h,2);

            break;


        case "DoubleImageButton":


            $("div.Main").append(" <input type='button' class='DoubleImageButton'/>");
            $("input.DoubleImageButton").removeClass("DoubleImageButton").addClass(typeId);

                $('input.'+typeId).click(function () {


                    var title=$(document).attr('title');


                    $.ajax({
                        url :  "onClick",	//请求url
                        type : "POST",	//请求类型  post|get
                        data : "titleName="+title+"&typeId="+typeId,	//后台用 request.getParameter("key");
                        dataType : "json",  //返回数据的 类型 text|json|html--
                        success : function(users){	//回调函数 和 后台返回的 数据



                        }
                    });

                });




            $('input.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w});
            $("input."+typeId).css({"color":user.textColor,"font-size":"15"});
            $("input."+typeId).attr('value',user.text);


            break;

        case "ChangeLabel":


            //alert(user.textSize+"::"+user.textColor);
            $("div.Main").append("  <font  class='ChangeLabel'></font>  ");
            $('font.ChangeLabel').removeClass("ChangeLabel").addClass(typeId);           
            $('font.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"font-size":user.textSize,"height":h,"width":w,'text-align':'center','color':user.textColor,'line-height':h+'px'});
			
			
			$('font.'+typeId).text(user.textValue);



            break;


        case "ChangeLabelBtn":


            $("div.Main").append("  <input type='text' class='ChangeLabelBtn' />  ");
            $('input.ChangeLabelBtn').removeClass("ChangeLabelBtn").addClass(typeId+'text');
            $('input.'+typeId+'text').css({"position":pos,'z-index':index,"left":x,"top":y,"height":h,"width":w*0.64,'color':'Red','fontSize':'20'});

            $("div.Main").append("  <input type='button' value='修改' class='ChangeLabelBtn' />  ");
            $('input.ChangeLabelBtn').removeClass("ChangeLabelBtn").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*0.65,"top":y,"height":h,"width":w*0.35,"color":"Black"});

			$('input.'+typeId+'button').val(user.value);


            $('input.'+typeId+'button').click(function () {


                var title=$(document).attr('title');


                //alert(title+":"+typeId+":"+$('input.'+typeId+'text').val());

                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+$('input.'+typeId+'text').val(),	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });

            });



            break;


        case "Pilar_A":



        $("div.Main").append("<div  class='Pilar_A'></div> ");
        $("div.Pilar_A").removeClass("Pilar_A").addClass(typeId);
        $("div."+typeId).attr('id',typeId);
        $("div."+typeId).css({"position":pos,'z-index':index,"left":x,"top":y-h/3,"height":h+h/3,"width":w});
        setWenduJi(typeId,user.datas);

        break;


        case "Pilar":


            $("div.Main").append("  <div  class='Pilar'></div>  ");
            $('div.Pilar').removeClass("Pilar").addClass(typeId);
            $('div.'+typeId).css({"position":pos,'z-index':index,"left":x,"top":y,"background-color":"transparent","height":h,"width":w,'border':'solid 1px #C0C0C0'});

            $("div.Main").append("  <div  class='Pilar'></div>  ");
            $('div.Pilar').removeClass("Pilar").addClass(typeId+"fill");
            $('div.'+typeId+"fill").css({"position":pos,'z-index':index,"left":x,"top":y+(h-user.datas/user.maxValue*h),"height":user.datas/user.maxValue*h,"width":w});

            if(user.datas>=(user.warmPer*user.maxValue))
            {
                $('div.'+typeId+"fill").css({"background-color":user.warmColor});
            }else
            {
                $('div.'+typeId+"fill").css({"background-color":user.normColor});
            }

            break;


        case "Ammeter":


            $("div.main").append("<div class='Ammeter'></div>")
            $("div.Ammeter").removeClass("Ammeter").addClass(typeId);
            $("div."+typeId).css({"position":pos,'z-index':index,"left":x-((1.2-1)*w)/2,"top":y-((1.2-1)*h)/2,"height":h*1.2,"width":w*1.2})
            $("div."+typeId).attr('id',typeId);
            setGrdata(typeId,"",user.minValue,user.maxValue,user.value,user.warmPer,user.borderColor,user.fillColor,user.lineColor,user.backgroundColor,user.warmPerColor);

            break;

        case "HisEvent":


            //alert(user.nameList);
            $('select.'+typeId+'equip').empty();

            for(var i=0; i<user.nameList.length; i++){

                $('select.'+typeId+'equip').append("<option class='opt'>123</option>");
                $('option.opt').removeClass("opt").addClass(typeId+'option'+i);
                $('option.'+typeId+'option'+i).text(user.nameList[i]);
            }


            break;
			
		case "TimingAndDelayed":


		
		   
		
           for(var i=0;i<6;i++)
		   {

                $("div.Main").append("  <font  class='TimingAndDelayed'></font>  ");
                $('font.TimingAndDelayed').removeClass("TimingAndDelayed").addClass(typeId+""+i);
		        $('font.'+typeId+""+i).css({"position":pos,'z-index':index,"left":x+w/10,"top":y + h * (i * 11) / 70.0,"height":h/10,"width":w*3/10,'color':'Black','fontSize':'20','text-align':'center','line-height':h/10+'px'});
				
				
				$("div.Main").append("  <input type='text' class='TimingAndDelayed' />  ");
                $('input.TimingAndDelayed').removeClass("TimingAndDelayed").addClass(typeId+'text'+i);
                $('input.'+typeId+'text'+i).css({"position":pos,'z-index':index,"left":x+w*4/10,"top":y+ h * (i * 11) / 70.0,"height":h/10,"width":w*3/10,'color':'Black','fontSize':'20','text-align':'center'});
              
			    
				if(i!=5)
				{
		            $('font.'+typeId+""+i).text("开启时间"+(i+1));
					if(i<user.tadList.length)
					{
						$('input.'+typeId+'text'+i).val(user.tadList[i].timing);
					}					
				}
				else
				{
					$('font.'+typeId+""+i).text("延时时间");
					
					$('input.'+typeId+'text'+5).val(user.tadList[0].delayed);
				
				}
				
		   }	   
				 
             
				 
		  	$("div.Main").append("  <input type='Button' class='TimingAndDelayed' value='确认' />  ");
            $('input.TimingAndDelayed').removeClass("TimingAndDelayed").addClass(typeId+'button');
            $('input.'+typeId+'button').css({"position":pos,'z-index':index,"left":x+w*3/10,"top":y+ h *63/ 70.0,"height":h/10,"width":w*3/10,'color':'Black','fontSize':'20','text-align':'center'});
        
          
            $('input.'+typeId+'button').click(function () {


                var title=$(document).attr('title');


                var value=$('input.'+typeId+'text'+0).val()+"-"+$('input.'+typeId+'text'+1).val()+"-"+$('input.'+typeId+'text'+2).val()+"-"+$('input.'+typeId+'text'+3).val()+"-"+$('input.'+typeId+'text'+4).val()+"-"+$('input.'+typeId+'text'+5).val();

			
				
                $.ajax({
                    url :  "onClick",	//请求url
                    type : "POST",	//请求类型  post|get
                    data : "titleName="+title+"&typeId="+typeId+"&value="+value,	//后台用 request.getParameter("key");
                    dataType : "json",  //返回数据的 类型 text|json|html--
                    success : function(users){	//回调函数 和 后台返回的 数据



                    }
                });

            });
            
			
			

            break;
			
			
    }


}

//画开关控件
function   setCri(user,id,x,y,w,h,index) {


    // $('#'+id).remove();
    // $("div.Main").append(" <canvas  class='Breaker' width='50px' height='50px'></canvas>");
    // $("canvas.Breaker").removeClass("Breaker").addClass(id);
    // $("canvas."+id).css({"position":user.pos,'z-index':user.index,"left":x,"top":y});
    // $("canvas."+id).attr('id',id);


    var m;

    if(w>h)
    {
        m=w;
    }else
    {
        m=h;
    }

    var c=document.getElementById(id);

    if(c.height>m)
    {
        c.height=m;
        c.width=m;
    }else
    {
        c.height=m+1;
        c.width=m+1;

    }





    var cxt=c.getContext("2d");

    cxt.translate(0.5*w,0.5*h);
    cxt.rotate((user.rotateAngle-90)*Math.PI/180);

    cxt.translate(-0.5*w,-0.5*h);

    cxt.strokeStyle=user.color;
    cxt.lineWidth=2;




    if(index==1)
    {
        cxt.moveTo(6*w/8,3*h/8);
        cxt.lineTo(w,5*h/8);

        cxt.moveTo(6*w/8,5*h/8);
        cxt.lineTo(w,3*h/8);
        cxt.stroke();
    }else if(index==2)
    {


        cxt.moveTo(w-w/8,h/3);
        cxt.lineTo(w-w/8,h-h/3);
        cxt.stroke();

    }




    cxt.beginPath();
    cxt.arc(h/8, h/2, h/8-1, 0, 2*Math.PI, true);
    cxt.closePath();


    cxt.moveTo(h/8,h/2);

    if(user.close)
    {

        cxt.lineTo(w,h/2-1);

    }else{



        cxt.lineTo(w,0);


    }
    cxt.stroke();


}


//定时更新页面 7s
function upadate(user,type,typeId, value){






    switch(type)
    {

        case "Label":


            $('font.' + typeId).text(value);
            $('font.'+typeId).css({'color':user.textColor});

            break;

        case "tigerLabel":




            $('font.' + typeId).text(value);



            break;

        case "AlarmLight":



            if(value==0)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel1.png');

            }else if(value==1)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel1.png');
            }else if(value==2)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel2.png');
            }else if(value==3)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel3.png');
            }else if(value==4)
            {
                $('img.'+typeId).attr("src",'image/AlarmLevel4.png');
            }





            break;

        case "SgClickPieChart":

            setPiedata(typeId,user);

            break;

        case "Dial":

            setCriData(typeId,user);

            break;

        case "EventList":

            $("table."+typeId).empty();

            for(var i=-1;i<user.data.length;i++)
            {
                $("table."+typeId).append(" <tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                if(i%2==0)
                {
                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.evenRowBackground});
                    }

                }else
                {

                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.oddRowBackground});
                    }

                }

                for(var j=0;j<5;j++)
                {
                    if(i==-1)
                    {

                        $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");
                    }else
                    {

                                $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");

                    }

                    var caa=typeId+'Td'+i+''+j;
                    $("td.Td").removeClass("Td").addClass(caa);
                    $("td."+caa).css({"width":user.wight/user.fromWight*window.screen.availWidth/5});
                    $("td."+caa).css({"text-align":'center'});
                  
					if(i!=-1)
                    {
                        $("td."+caa).html(user.data[i][j]);
                    }else {

                        $("td."+caa).html(user.lstTitles[j]);
                    }

					


                }
            }



            break;


        case "SignalList":

            $("table."+typeId).empty();

            for(var i=-1;i<user.data.length;i++)
            {
                $("table."+typeId).append(" <tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                if(i%2==0)
                {
                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.evenRowBackground});
                    }

                }else
                {

                    if(i==-1)
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":'gray',"background":'transparent'});

                    }else
                    {
                        $("tr."+typeId+'Tr'+i).css({"color":user.foreColor,"background":user.oddRowBackground});
                    }

                }

                for(var j=0;j<5;j++)
                {
                 
				  $("tr."+typeId+'Tr'+i).append("<td class='Td'>user.data[i][j]</td>");

                    var caa=typeId+'Td'+i+''+j;
                    $("td.Td").removeClass("Td").addClass(caa);
                    $("td."+caa).css({"width":user.wight/user.fromWight*window.screen.availWidth/5});
                    $("td."+caa).css({"text-align":'center'});
                    if(i!=-1)
                    {
                        $("td."+caa).html(user.data[i][j]);
                    }else
                    {
                        $("td."+caa).html(user.lstTitles[j]);
                    }



                }
            }




            break;


        case "Dial_C":


            setGrdata(typeId,"",user.minValue,user.maxValue,user.value,user.warmPer,user.borderColor,user.fillColor,user.lineColor,user.backgroundColor,user.warmPerColor);

            break;


        case "AutoSigList":




            setLinedata(typeId,user,map[typeId]);

            break;

        case "SMSConfig":


            var le=Object.keys(user.map).length;


            if(le>0)
            {
                for(var x in user.map){

				    var text=user.map[x];
				   
                    if(x=="name")
                    {
						
                        //$("input."+typeId+'text'+1).attr('value',text);
						$("input."+typeId+'text'+1).val(text);
                    }
                    if(x=="tel_number")
                    {
                        //$("input."+typeId+'text'+2).attr('value',text);
						$("input."+typeId+'text'+2).val(text);
                    }
                    if(x=="alarm_level")
                    {
                       // $("input."+typeId+'text'+3).attr('value',text);
					   $("input."+typeId+'text'+3).val(text);
                    }
                }
            }else
            {
                var idF = $("input."+typeId+'text'+1).is(':focus');
                var pwF = $("input."+typeId+'text'+2).is(':focus');
                var timeF = $("input."+typeId+'text'+3).is(':focus');

                if(idF||pwF||timeF)
                {

                }else
                {
                 $("input."+typeId+'text'+1).val("");
                 $("input."+typeId+'text'+2).val("");
                 $("input."+typeId+'text'+3).val("");
                }

              
            }


            break;

        case "SgSplineChart":


            setLineChart(typeId,user,map[typeId]);

            break;

        case "StatePanel":


            if(user.value==0)
            {
                $('img.'+typeId).attr("src",'image/normal.png');

            }else if(user.value==1)
            {
                $('img.'+typeId).attr("src",'image/error.png');
            }else if(user.value==2)
            {
                $('img.'+typeId).attr("src",'image/warning.png');
            }

            break;

        case "ELabel":


            $('font.' + typeId).text(user.text);
            $('font.'+typeId).css({'color':user.textColor});

            break;

        case "AlarmCount":


            $('font.' + typeId).text(user.text);


            break;

        case "RC_Label":





            break;

        case "SgBarChartView":


            if(user.math)
            {
                setNewBardata(typeId,"电能",user, sgBarMap[typeId]);
            }else
            {

                setOldBardata(typeId,"温度",user);
            }


            break;


        case "SgAlarmActionShow":

            $('font.' + typeId).text(user.text);

            break;

        case "StateButton":


            $('img.'+typeId).attr("src",user.imagePath);

            break;


        case "IsolationSwitch":


            var x=user.left/user.fromWight*window.screen.availWidth;
            var y=user.top/user.fromHeight*window.screen.availHeight;
            var h=user.heght/user.fromHeight*window.screen.availHeight;
            var w=user.wight/user.fromWight*window.screen.availWidth;

            setCri(user,typeId,x,y,w,h,2);

            break;

        case "Breaker":


            var x=user.left/user.fromWight*window.screen.availWidth;
            var y=user.top/user.fromHeight*window.screen.availHeight;
            var h=user.heght/user.fromHeight*window.screen.availHeight;
            var w=user.wight/user.fromWight*window.screen.availWidth;

            setCri(user,typeId,x,y,w,h,1);

            break;

        case "StartAndEndTriggerSet":



            $("font."+typeId+"2").text(user.startValue);
            $("font."+typeId+"5").text(user.stopValue);

            break;

        case "AlarmLevel":

            $("table."+typeId).empty();

            for(var i=0;i<user.list.length;i++)
            {

                $("table."+typeId).append(" <tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tr'+i);
                $("tr."+typeId+'Tr'+i).css({"color":'#00ffff',"background":user.lineColor});

                $("tr."+typeId+'Tr'+i).append("<td class='Td'></td>");
                $("td.Td").removeClass("Td").addClass(typeId+'Td'+i);
                $("td."+typeId+'Td'+i).css({"width":user.wight/user.fromWight*window.screen.availWidth/6,"text-align":'center'});
                $("td."+typeId+'Td'+i).append("<img  class='AlarmLevel' alt='fail'/>");

                $("img.AlarmLevel").removeClass("AlarmLevel").addClass(typeId+i);


                if(user.list[i].img==2130837518)
                {
                    $('img.'+typeId+i).attr("src",'image/hk.png');

                }else if(user.list[i].img==2130837516)
                {
                    $('img.'+typeId+i).attr("src",'image/hi.png');

                }else if(user.list[i].img==2130837517)
                {
                    $('img.'+typeId+i).attr("src",'image/hj.png');
                }




                $("tr."+typeId+'Tr'+i).append("<tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Tro'+i);

                $("tr."+typeId+'Tro'+i).css({"color":user.titleColor,"background":user.lineColor});

                $("tr."+typeId+'Tro'+i).append("<td class='Td'>2018.11.06 11:33:05</td>");
                $("td.Td").removeClass("Td").addClass(typeId+'Tdo'+i);
                $("td."+typeId+'Tdo'+i).css({"width":user.wight/user.fromWight*window.screen.availWidth*5/6});
                $("td."+typeId+'Tdo'+i).html(user.list[i].time);


                $("tr."+typeId+'Tr'+i).append("<tr class='Tr'></tr>");
                $("tr.Tr").removeClass("Tr").addClass(typeId+'Trt'+i);

                $("tr."+typeId+'Trt'+i).css({"color":user.infoColor,"background":user.lineColor});

                $("tr."+typeId+'Trt'+i).append("<td class='Td'>温湿度-COM2--设备通讯状态:中断 等级:严重告警</td>");
                $("td.Td").removeClass("Td").addClass(typeId+'Tdt'+i);
                $("td."+typeId+'Tdt'+i).css({"width":user.wight/user.fromWight*window.screen.availWidth*5/6});
                $("td."+typeId+'Tdt'+i).html(user.list[i].value);


            }





            break;



        case "SgHalfCircleChar":



            setGrdata2(typeId,"",user.minValue,user.maxValue,user.value,user.listValue,user.listColor);

            break;


        case "ChangeUserInfo":



            var le=Object.keys(user.mapData).length;

            if(le>0)
            {
                for(var x in user.mapData){



                    if(x=="uid")
                    {

                        $("input."+typeId+'text'+1).attr('value',user.mapData[x]);
                    }
                    if(x=="pw")
                    {
                        $("input."+typeId+'text'+2).attr('value',user.mapData[x]);
                    }
                    if(x=="time")
                    {
                        $("input."+typeId+'text'+3).attr('value',user.mapData[x]);
                    }
                }
            }else
            {


                var idF = $("input."+typeId+'text'+1).is(':focus');
                var pwF = $("input."+typeId+'text'+2).is(':focus');
                var timeF = $("input."+typeId+'text'+3).is(':focus');

                if(idF||pwF||timeF)
                {

                }else
                {
                    $("input."+typeId+'text'+1).val("");
                    $("input."+typeId+'text'+2).val("");
                    $("input."+typeId+'text'+3).val("");
                }

            }


            break;




        case "DoubleImageButton":



            $("input."+typeId).css({"color":user.textColor,"font-size":"15"});
            $("input."+typeId).attr('value',user.text);


            break;


        case "ChangeLabel":



           // alert("456::"+user.text);

            $('font.'+typeId).text(user.textValue);





            break;

        case "Rectangle":





            if(user.bgColor=="#FFFFFFFF")
            {

            }else{


                $('div.'+typeId).css({"background-color":user.bgColor});

                // if(user.alpha!=0)
                // {
                //     $('div.'+typeId).css({"opacity":user.alpha/255});
                // }

            }

            break;


        case "Image":


            $('img.'+typeId).attr("src",user.imagePath);

            break;


        case "Pilar":


            var x=user.left/user.fromWight*window.screen.availWidth;
            var y=user.top/user.fromHeight*window.screen.availHeight;
            var h=user.heght/user.fromHeight*window.screen.availHeight;
            var w=user.wight/user.fromWight*window.screen.availWidth;


            $('div.'+typeId+"fill").css({"left":x,"top":y+(h-user.datas/user.maxValue*h),"height":user.datas/user.maxValue*h,"width":w});

            if(user.datas>=(user.warmPer*user.maxValue))
            {
                $('div.'+typeId+"fill").css({"background-color":user.warmColor});
            }else
            {
                $('div.'+typeId+"fill").css({"background-color":user.normColor});
            }

            break;


        case "Pilar_A":


            setWenduJi(typeId,user.datas); //num.toFixed(2)

            break;

        case "Ammeter":

            setGrdata(typeId,"",user.minValue,user.maxValue,user.value,user.warmPer,user.borderColor,user.fillColor,user.lineColor,user.backgroundColor,user.warmPerColor);

            break;
			
			
		case "TimingAndDelayed":


		
           for(var i=0;i<6;i++)
		   {

				if(i!=5)
				{
		           
					if(i<user.tadList.length)
					{
						$('input.'+typeId+'text'+i).val(user.tadList[i].timing);
					}else
					{
                        $('input.'+typeId+'text'+i).val("");
					}				
				}
				else
				{

					$('input.'+typeId+'text'+5).val(user.tadList[0].delayed);
				
				}
				
		   }	   
				 
             
				 
		  
        
          
            

            break;


    }


}


//设置Cookie
function setCookie(cname,cvalue,exdays){
    var d = new Date();
    d.setTime(d.getTime()+(exdays*1000));


    var expires = "expires="+d.toGMTString();
    //document.cookie = cname+"="+cvalue+"; "+expires;  //设置时间
    document.cookie = cname+"="+cvalue;   //默认关闭浏览器cookie失效
}

//获取Cookie
function getCookie(cname){
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
         //var c = ca[i].trim();
        var c = jQuery.trim(ca[i]);
        //alert(c);
        if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
    }
    return "";
}

//date转str
function    getDateStr(dataValue) {

    var  time=dataValue.getFullYear() + "-" +((dataValue.getMonth()+1)<10?"0":"")+(dataValue.getMonth()+1)+"-"+(dataValue.getDate()<10?"0":"")+dataValue.getDate();
    return time;
}


//str转date
function    getDate(dataValue) {

    var str = dataValue.toString();
    str = str.replace(/-/g, "/");
    var oDate1 = new Date(str);
    return oDate1;
}

//时间刷新
function  displayTime(user) {

    var times=new Date();

    var y=times.getFullYear();
    var m=times.getMonth()+1;
	
	
	
    if(m<10)
    {
        m='0'+m;
    }

    var d=times.getDate();
    if(d<10)
    {
        d='0'+d;
    }

    var h=times.getHours();
    var min=times.getMinutes();
    var s=times.getSeconds();

    if(h<10)
    {
        h='0'+h;
    }

    if(min<10)
    {
        min='0'+min;
    }

    if(s<10)
    {
        s='0'+s;
    }

    var week;
	
	if(user.language=="Chinese")
	{
	if(times.getDay()==0) week="星期日"
    if(times.getDay()==1) week="星期一"
    if(times.getDay()==2) week="星期二"
    if(times.getDay()==3) week="星期三"
    if(times.getDay()==4) week="星期四"
    if(times.getDay()==5) week="星期五"
    if(times.getDay()==6) week="星期六"
	}else{
	if(times.getDay()==0) week="Sunday"
    if(times.getDay()==1) week="Monday"
    if(times.getDay()==2) week="Tuesday"
    if(times.getDay()==3) week="Wednesday"
    if(times.getDay()==4) week="Thursday"
    if(times.getDay()==5) week="Friday"
    if(times.getDay()==6) week="Saturday"
		
	}
    

    var time=y+'-'+m+'-'+d+' '+h+':'+min+':'+s+' '+week;

    $('font.'+user.typeId).text(time);

    setTimeout(function(){ displayTime(user)},1000);

}

//是否是数字
function isNumber(value) {
    var patrn = /^(-)?\d+(\.\d+)?$/;
    if (patrn.exec(value) == null || value == "") {
        return false
    } else {
        return true
    }
}






var map = {};
var sgBarMap = {};