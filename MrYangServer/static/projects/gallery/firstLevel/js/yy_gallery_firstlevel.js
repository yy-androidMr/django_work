var level1_dir;
var media_root = '/static/media';
var pre_path;//指定到thum目录
var page_max_album = 20; //页签控制,一页最多多少个相册
$(document).ready(function () {
        picPage()
    }
);

function loadTitle() {
    var parent = $('#page_title_parent');
    var tilte_count = level1_dir.length / page_max_album + 1;
    for (var i = 0; i < tilte_count; i++) {
        var item = $('#page_title_item').clone(true);
        item.removeAttr('hidden');
        item.removeAttr('id');
        // active selected
        var class_attr = i == 0 ? 'nav-item active selected' : 'nav-item';
        item.attr('class', class_attr);
        var pagedata = item.find('#page_title_item_data');
        pagedata.attr('data-no', '' + (i + 1));
        parent.append(item);
    }
}

function picPage() {
    loadTitle();
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
        pTag.html(data_item.intro + '<br>' + data_item.time);
        var itemImg = item.find('#pic_thum');
        itemImg.attr('src', media_root + pre_path + data_item.rel_path + '/' + data_item.thum);
        parent.append(item);

    }


}


function convert_pic(dirsJson, path) {
    pre_path = path;
    var dirs = new Array();
    for (var i = 0, count = dirsJson.length; i < count; i++) {
        var item = dirsJson[i];
        dirs[i] = {
            id: item.id,
            // name: null,
            // tags: item.tags,
            rel_path: item.rel_path,
            c_id: item.c_id,
        }
        if (item.tags[0].length != 0) {
            dirs[i].name = item.tags[0];//dir_split[dir_split.length - 1];
        } else {
            dirs[i].name = '暂未命名';//dir_split[dir_split.length - 1];
        }
        if (item.tags.length > 1) {
            if (item.tags[1].length != 0) {
                dirs[i].intro = item.tags[1];//dir_split[dir_split.length - 1];
            } else {
                dirs[i].intro = '没有任何描述';
            }
        }
        dirs[i].time = '';
        if (item.tags.length > 2) {
            dirs[i].time = item.tags[2];//dir_split[dir_split.length - 1];
        }

        if (item.tags.length > 3) {
            dirs[i].thum = item.tags[3];//dir_split[dir_split.length - 1];
            // 这里没有临时文件
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