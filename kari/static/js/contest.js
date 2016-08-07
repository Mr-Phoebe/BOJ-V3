/*
var cnt = 0;
var noticeList = new Array();
window.onload = function() {
	var probs = document.getElementsByName("problem_id");
	cnt = probs.length;
	fetchNotice();
	setInterval(function(){fetchNotice()},60000);
}
*/

/*
function addRecentProb(id) {
	var probId = document.getElementById("recent_problem_id_"+id);
	var probTtl = document.getElementById("recent_problem_title_"+id);
	addProb();
	document.getElementById("problem_id_"+(cnt-1)).value = probId.innerHTML;
	document.getElementById("problem_title_custom_"+(cnt-1)).value = probTtl.innerHTML;
	document.getElementById("problem_title_"+(cnt-1)).innerHTML = probTtl.innerHTML;
}

function delProb(id) {
	var probTbl = document.getElementById("problem_table");
	var prob = document.getElementById("problem_"+id);
	probTbl.deleteRow(prob.rowIndex);
}

function addProb() {
	var probTbl = document.getElementById("problem_table");
	var newProb = probTbl.insertRow(probTbl.rows.length);
	newProb.setAttribute("id", "problem_"+cnt);
	var newMdfy = newProb.insertCell(0);
	var newId = newProb.insertCell(1);
	var newTtlCus = newProb.insertCell(2);
	var newTtl= newProb.insertCell(3);
	var str;
	newMdfy.setAttribute("class", "problem_modify");
	newMdfy.innerHTML='<button type="button" onclick="delProb('+cnt+')">删除</button>';
	str='"problem_id_'+cnt+'"';
	newId.innerHTML='<input type="text" name="problem_id" id='+str+' onchange="checkProblem('+cnt+')">';
	str='problem_title_custom_'+cnt;
	newTtlCus.innerHTML='<input type="text" name="problem_title_custom" id='+str+'>';
	str='problem_title_'+cnt;
	newTtl.setAttribute("class", "problem_title");
	newTtl.setAttribute("id", str);
	newTtl.innerHTML='题目不存在!';
	cnt++;
}
*/

function getProb(pid) {
    if (!(parseInt(pid)>0)) return null;
    var t = $.ajax({
		type: "POST",
		url: probTtlUrl,
		data: {"pid": pid},
        async: false
	}).responseText;
    return t;
}

function setTitle(p, title) {
    var row = $(p).parent().parent();
    if (title) {
        $(row).find("span.problem_title").text(title);
        $(row).find("input[name='problem_title_custom']").val(title);
    } else {
        $(row).find("span.problem_title").text("题目不存在");
        $(row).find("input[name='problem_title_custom']").val("");
    }
}

function checkProb(p, keepTitle) {
    var title = getProb($(p).val());
    if (!keepTitle) setTitle(p, title);
    if (title)
        return true;
    else {
        alert("不能使用不存在的题目！");
        $(p).focus();
        return false;
    }
}

function addProb(pid) {
    var list = $("table#problem_table tbody");
    var last = $(list).find("tr.prob_element:last");
    var newpid = null;
    if (pid) {
        newpid = pid.toString();
    } else {
        newpid = (function(last){
            var pid = parseInt($(last).find("input[name='problem_id']").val());
            if (pid > 0) return (pid+1).toString();
            else return '';
        })(last);
    }
    $(list).append($(last).clone());
    last = $(list).find("tr.prob_element:last");
    var p = $(last).find("input[name='problem_id']");
    $(p).val(newpid);
    var title = getProb(newpid);
    setTitle(p, title);
    /*
    $(last).find("input[name='problem_id']").val(newpid);
    var title = null;
    if (parseInt(newpid)>0)
        title = getProb(newpid);
    if (title) $(last).find("span.problem_title").text(title);
    else $(last).find("span.problem_title").text('题目不存在');
    */
    $(last).removeClass('hide');

    var cnt = $(list).find("input[name='problem_id']").length;
    if (cnt >= 26+1) {
        $("button.add-prob-btn").attr("disabled", true);
    }
}

function addRecentProb(p) {
    var pid = $(p).parent().parent().find("span.recent_problem_id").text();
    addProb(parseInt(pid));
}

function delProb(p) {
    $(p).parent().parent().remove();
    var cnt = $("table#problem_table tbody").find("input[name='problem_id']").length;
    if (cnt < 26+1) {
        $("button.add-prob-btn").attr("disabled", false);
    }
}

function checkAllProb() {
    var list = $("table#problem_table tbody");
    var check = true;
    var pidList = new Array();
    $(list).find("input[name='problem_id']").each(function(i, e){
        if (!($(e).parent().parent().hasClass("hide"))) {
            check = checkProb(e, true);
            var pid = $(e).val();
            if (pidList[pid]) {
                alert('不能添加重复的题目！');
                check = false;
            } else {
                pidList[pid] = true;
            }
            if (i > 25) {
                alert('不能添加超过26道题目！');
                check = false;
            }
            if (!check) {
                $(e).focus();
                return false;
            }
        }
    });
    if (check) {
        $(list).find("tr.hide").remove();
        return true;
    } else {
        return false;
    }
}
/*
function checkProblem(id) {
	var pid = $("#problem_id_"+id).val();
	$.ajax({
		type: "POST",
		url: probTtlUrl,
		data: {"pid": pid},
		success: function(data) {
			if(data.length == 0) {
				alert("不能使用不合法的题目!");
			}
			else {
				$("#problem_title_"+id).html(data);
				document.getElementById("problem_title_custom_"+id).value = data;
			}
		}
	});
}

function checkAllProblem() {
	var validCnt = 0;
	for(var i = 0; i < cnt; i++) {
		var prob = document.getElementById("problem_"+i);
		if (prob) {
			var pTtl = document.getElementById("problem_title_"+i).innerHTML;
			if(pTtl == '题目不存在!') {
				alert("不能使用不合法的题目!");
				return false;
			}
			validCnt++;
		}
	}
	if (validCnt <= 0) {
		alert("请至少添加一道题目!");
		return false;
	}
	if (validCnt > 26) {
		alert('考试中的题目不能超过26道!');
		return false;
	}
	return true;
}
*/

function fetchNotice() {
	$.ajax({
		type: "POST",
		url: "/Contest/getContestNoticeList/",
		data: {"cid": cid},
		success: function(data) {
			if(data.length > 0) {
				document.getElementById("contest_notice").innerHTML = data;
			}
		}
	});
}
