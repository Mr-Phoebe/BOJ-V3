var cnt = 0;
/*
window.onload = function() {
	var probs = document.getElementsByName("problem_id");
	cnt = probs.length;
}
*/
function delData(id) {
	var dataTbl = document.getElementById("data_table");
	var data = document.getElementById("data_"+id);
	dataTbl.deleteRow(data.rowIndex);
}

function addData() {
	var dataTbl = document.getElementById("data_table");
	var newData = dataTbl.insertRow(dataTbl.rows.length);
	newData.setAttribute("id", "data_"+cnt);
	var newMdfy = newData.insertCell(0);
	var newIn = newData.insertCell(1);
	var newOut = newData.insertCell(2);
	var newScr = newData.insertCell(3);
	var str;
	newMdfy.setAttribute("class", "data_modify");
	newMdfy.innerHTML='<button type="button" onclick="delData('+cnt+')">删除</button>';
	str='"data_in_'+cnt+'"';
	newIn.innerHTML='<input type="file" name="data_in" id='+str+'>';
	str='"data_out_'+cnt+'"';
    newOut.innerHTML='<input type="file" name="data_out" id='+str+'>';
	str='"data_score_'+cnt+'"';
	newScr.innerHTML='<input tpye="text" name="data_scr" id='+str+' value="100">';
	cnt++;
}

function checkAllData() {
    if (document.getElementById('id_change_data').value==0)
        return true;
	var validCnt = 0;
	for(var i = 0; i < cnt; i++) {
		var data = document.getElementById("data_"+i);
		if (data) {
			validCnt++;
            infile = document.getElementById("data_in_"+i);
            if (!(infile.value)){
                alert("No file in the "+validCnt+" data input!");
                return false;
            }
            outfile = document.getElementById("data_out_"+i);
            if (!(outfile.value)){
                alert("No file in the "+validCnt+" data output!");
                return false;
            }
            scr = document.getElementById("data_src_"+i);
            if (!(scr.value)){
                alert("No score in the "+validCnt+" data score!");
                return false;
            }
		}
	}
	if (validCnt <= 0) {
		alert("At least one pair of data!");
		return false;
	}
	return true;
}
