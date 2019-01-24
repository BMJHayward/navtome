parseFasta = (fileObj) =>
{
	var fileSections = [];
	var lines = fileObj.split(/\r\n|\n/);
	lines.forEach((line) => {
		if (line[0] == '>'){
		    /*add to description*/
		    fileSections.push({ desc: line.slice(1), data: '' });
		}
    	else if (line == /\r\n|\n/){/*blank line, do nothing*/}
	    else {
		    fileSections[fileSections.length-1].data += line;
		}
	})
	return fileSections;
};

parseGenbank = (fileObj) =>
{
    var fileSections = [];
    var lines = fileObj.split(/\r\n|\n/);
    var featIdx;
    var originIdx;
    lines.forEach((line) => {
        if (line.toUpperCase().includes('FEATURES')) {featIdx = lines.indexOf(line)};
        if (line.toUpperCase().includes('ORIGIN')) {originIdx = lines.indexOf(line)};
    });
    fileSections.push({ desc: 'metadata', data: lines.slice(0, featIdx)});
    fileSections.push({ desc: 'features', data: lines.slice(featIdx + 1, originIdx)});
    fileSections.push({ desc: 'origin', data: lines.slice(originIdx + 1)});
    return fileSections;
};

getFileText = (fileName, fileType, fileData) =>
{
    switch (fileType) {
        case 'fasta':
        case 'fa':
          return parseFasta(fileData);
        case 'genbank':
        case 'gb':
        case 'gbk':
          return parseGenbank(fileData);
        default:
          return [{'desc':fileName, 'data':fileData}];
    };
};

var loadFile = function(event) {
	var input = event.target;
	var fname = input.files[0].name;
	var ftype = fname.substring(fname.lastIndexOf('.') + 1, fname.length) || fname;
	var reader = new FileReader();
	reader.readAsText(input.files[0]);
	reader.onload = function(e) {
	    var textZone = document.getElementById('textZone');
	    while (textZone.firstChild) textZone.removeChild(textZone.firstChild);
	    var textBlocks = getFileText(fname, ftype, reader.result);
	    textBlocks.forEach((textBlock) =>
	        {
	            var zoneItem = document.createElement('li');
	            var innerDesc = document.createElement('h4');
	            innerDesc.innerHTML = textBlock.desc;
	            innerDesc.style += 'bold';
	            var innerText = document.createElement('textarea');
	            innerText.innerHTML = textBlock.data;
	            zoneItem.appendChild(innerDesc)
	            zoneItem.appendChild(innerText);
	            textZone.appendChild(zoneItem);
	        });
	};
};