/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
    config.ImageUpload = true;
    config.ImageBrowser = true;

    //*
    // 换行方式
    config.enterMode = CKEDITOR.ENTER_BR;
    // 当输入：shift+Enter是插入的标签
    config.shiftEnterMode = CKEDITOR.ENTER_BR;//
    //图片处理
    config.pasteFromWordRemoveStyles = true;
    config.filebrowserImageUploadUrl = "ckUploadImage.action?type=image";
    // 去掉ckeditor“保存”按钮
    config.removePlugins = 'save';
    //*/
};
