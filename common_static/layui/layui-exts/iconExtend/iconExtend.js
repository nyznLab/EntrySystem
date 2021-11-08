/**
 * layui 扩展插件：layui图标扩展
 * 版本：v1.0
 * 作者：zhiqiang94@vip.qq.com
 * 更新时间：2020-12-16 20:21:59
 */
layui.define(['jquery'], function (exports) {
    var $ = jquery = layui.jquery;
    var MOD_NAME = 'iconExtend', ICON_CSS_FOLDER_NAME = 'iconfont', ICON_CLASS = ['layui-icon', 'layui-icon-extend'], ICON_PREFIX = 'layui-extend-';
    layui.link(layui.cache.base + MOD_NAME + '/' + MOD_NAME + '.css');

    function IconDom() {
        return {
            id: '',
            dom: null,
            className: '',
            on: function (events_, callback_) {
                return $(this.dom).on(events_, callback_);
            },
            style: function (key, value) {
                if (key) {
                    if (Object.prototype.toString.call(key) === '[object Object]') {
                        var this_ = this;
                        Object.keys(key).forEach(key_ => $(this_.dom).css(key_, key[key_]));
                    } else {
                        if (value) {
                            $(this.dom).css(key, value);
                        } else {
                            try {
                                return $(this.dom).css(key);
                            } catch (e) {
                                return this;
                            }
                        }
                    }
                }
                return this;
            },
            fontSize: function (fontSize) {
                return this.style('font-size', fontSize);
            },
            color: function (color) {
                return this.style('color', color);
            },
            change: function (className_) {
                this.dom.classList.remove(this.className);
                if (className_) {
                    className_ = (className_ && className_.indexOf(ICON_PREFIX) != 0) ? ICON_PREFIX + className_ : className_;
                    this.dom.classList.add(className_);
                }
                this.className = className_;
                return this;
            },
            show: function () {
                $(this.dom).show();
            },
            hide: function () {
                $(this.dom).hide();
            },
            remove: function () {
                $(this.dom).remove();
            }
        }
    }

    // iconExtend构造器
    var iconExtendClass = function (projectName_, options_) {
        this.loadProject(projectName_, options_);
    };
    iconExtendClass.prototype = {
        options: {
            style: {},
            icon_class: ICON_CLASS,
        },
        loadProject: function (projectName_, options_) {
            if (projectName_) {
                layui.link(layui.cache.base + 'iconExtend/' + ICON_CSS_FOLDER_NAME + '/' + projectName_ + '/iconfont.css', 'iconExtend-' + projectName_);
            }
            this.options = $.extend({}, this.options, options_);
            if(options_ && options_.icon_class){
                this.options.icon_class = ICON_CLASS.concat(options_.icon_class);
            }
            return this;
        },
        on: function (events_, callback_) {
            return $('.layui-icon-extend').on(events_, callback_);
        },
        createIcon: function (className_, styles_) {
            // uuid
            var d_ = new Date().getTime();
            var id_ = 'zxxx-qxxxx-9xxx-4xxx'.replace(/[xy]/g, function (c) {
                var r = (d_ + Math.random() * 16) % 16 | 0;
                d_ = Math.floor(d_ / 16);
                return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
            // 创建dom对象
            var icon_dom_ = document.createElement('i');
            this.options.icon_class.forEach(class_ => icon_dom_.classList.add(class_));
            icon_dom_.classList.add(id_);
            if (className_) {
                className_ = (className_ && className_.indexOf(ICON_PREFIX) != 0) ? ICON_PREFIX + className_ : className_;
                icon_dom_.classList.add(className_);
            }
            var new_styles_ = $.extend({}, this.options.style, styles_);
            if (new_styles_) {
                Object.keys(new_styles_).forEach(key => $(icon_dom_).css(key, new_styles_[key]));
            }
            // 创建icon对象
            var iconDom = new IconDom();
            iconDom.id = id_;
            iconDom.className = className_;
            iconDom.dom = icon_dom_;
            return iconDom;
        },
        prepend: function (appDom_, className_, styles_) {
            var iconDom = this.createIcon(className_, styles_);
            // 追加到指定dom最前
            if (appDom_) {
                $(appDom_).prepend(iconDom.dom);
            }
            return iconDom;
        },
        append: function (appDom_, className_, styles_) {
            var iconDom = this.createIcon(className_, styles_);
            // 追加到指定dom最后
            if (appDom_) {
                $(appDom_).append(iconDom.dom);
            }
            return iconDom;
        }
    };

    var projects = {};

    //外部接口
    var iconExtend = {
        // 事件监听
        on: function (events, callback) {
            return layui.onevent.call(this, ICON_CSS_FOLDER_NAME, events, callback);
        }
    };
    //核心入口
    iconExtend.loadProject = function (projectName_, options_) {
        // 第一次加载的项目 则新建iconExtendClass对象
        if (!projects[projectName_]) {
            projects[projectName_] = new iconExtendClass(projectName_, options_);
        } else {
            // 否则只用更新配置
            projects[projectName_].loadProject(projectName_, options_);
        }
        return projects[projectName_];
    };

    //输出接口
    exports(MOD_NAME, iconExtend);
});