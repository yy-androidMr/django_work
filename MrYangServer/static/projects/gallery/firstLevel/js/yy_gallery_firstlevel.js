var level1_dir;

$(document).ready(function () {
        picPage()
    }
);

function picPage() {
// testJson
//     window.alert($('#testJson'))
//     $('#testJson').html(js_dir[0].name);
    var parent = $('#gallery_pool');
    for (var i = 0; i < level1_dir.length; i++) {
        var data_item = level1_dir[i];
        var item = $('#pic_item').clone(true);
        item.removeAttr('hidden');
        item.removeAttr('id');

        var h2Tag = item.find('#item_name');
        h2Tag.html(data_item.name);
        var pTag = item.find('#item_intro');
        pTag.html(data_item.intro+'<br>'+data_item.time);


        parent.append(item);

    }


}


function convert_pic(dirsJson) {
    var dirs = new Array();
    for (var i = 0, count = dirsJson.length; i < count; i++) {
        var item = dirsJson[i];
        dirs[i] = {
            id: item.id,
            // name: null,
            // tags: item.tags,
            c_id: item.c_id,

        }
        dirs[i].name = item.tags[0];//dir_split[dir_split.length - 1];
        dirs[i].intro = '没有任何描述';
        if (item.tags.length > 1) {
            dirs[i].intro = item.tags[1];//dir_split[dir_split.length - 1];
        }
        dirs[i].time = '';
        if (item.tags.length > 2) {
            dirs[i].time = item.tags[2];//dir_split[dir_split.length - 1];
        }

        // if (item.p_id != null) {
        //     dirs[i].parent = item.p_id;
        // } else {
        //     dirs[i].parent = -1;
        //     rootDir = dirs[i];
        // }
    }
    level1_dir = dirs;

}