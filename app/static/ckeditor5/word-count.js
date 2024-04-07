!function(t){const e=t.en=t.en||{};e.dictionary=Object.assign(e.dictionary||{},{"Characters: %0":"Characters: %0","Words: %0":"Words: %0"})}(window.CKEDITOR_TRANSLATIONS||(window.CKEDITOR_TRANSLATIONS={})),
/*!
 * @license Copyright (c) 2003-2023, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md.
 */(()=>{var t={704:(t,e,r)=>{t.exports=r(79)("./src/core.js")},273:(t,e,r)=>{t.exports=r(79)("./src/ui.js")},209:(t,e,r)=>{t.exports=r(79)("./src/utils.js")},79:t=>{"use strict";t.exports=CKEditor5.dll}},e={};function r(o){var n=e[o];if(void 0!==n)return n.exports;var i=e[o]={exports:{}};return t[o](i,i.exports,r),i.exports}r.d=(t,e)=>{for(var o in e)r.o(e,o)&&!r.o(t,o)&&Object.defineProperty(t,o,{enumerable:!0,get:e[o]})},r.o=(t,e)=>Object.prototype.hasOwnProperty.call(t,e),r.r=t=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})};var o={};(()=>{"use strict";r.r(o),r.d(o,{WordCount:()=>z});var t=r(704),e=r(273),n=r(209);function i(t){if(t.is("$text")||t.is("$textProxy"))return t.data;const e=t;let r="",o=null;for(const t of e.getChildren()){const e=i(t);o&&o.is("element")&&(r+="\n"),r+=e,o=t}return r}const s=function(t){var e=typeof t;return null!=t&&("object"==e||"function"==e)};const c="object"==typeof global&&global&&global.Object===Object&&global;var a="object"==typeof self&&self&&self.Object===Object&&self;const u=c||a||Function("return this")();const d=function(){return u.Date.now()};var l=/\s/;const f=function(t){for(var e=t.length;e--&&l.test(t.charAt(e)););return e};var h=/^\s+/;const p=function(t){return t?t.slice(0,f(t)+1).replace(h,""):t};const g=u.Symbol;var v=Object.prototype,b=v.hasOwnProperty,w=v.toString,y=g?g.toStringTag:void 0;const _=function(t){var e=b.call(t,y),r=t[y];try{t[y]=void 0;var o=!0}catch(t){}var n=w.call(t);return o&&(e?t[y]=r:delete t[y]),n};var m=Object.prototype.toString;const j=function(t){return m.call(t)};var x=g?g.toStringTag:void 0;const O=function(t){return null==t?void 0===t?"[object Undefined]":"[object Null]":x&&x in Object(t)?_(t):j(t)};const T=function(t){return null!=t&&"object"==typeof t};const C=function(t){return"symbol"==typeof t||T(t)&&"[object Symbol]"==O(t)};var S=/^[-+]0x[0-9a-f]+$/i,E=/^0b[01]+$/i,W=/^0o[0-7]+$/i,N=parseInt;const P=function(t){if("number"==typeof t)return t;if(C(t))return NaN;if(s(t)){var e="function"==typeof t.valueOf?t.valueOf():t;t=s(e)?e+"":e}if("string"!=typeof t)return 0===t?t:+t;t=p(t);var r=E.test(t);return r||W.test(t)?N(t.slice(2),r?2:8):S.test(t)?NaN:+t};var V=Math.max,L=Math.min;const R=function(t,e,r){var o,n,i,c,a,u,l=0,f=!1,h=!1,p=!0;if("function"!=typeof t)throw new TypeError("Expected a function");function g(e){var r=o,i=n;return o=n=void 0,l=e,c=t.apply(i,r)}function v(t){var r=t-u;return void 0===u||r>=e||r<0||h&&t-l>=i}function b(){var t=d();if(v(t))return w(t);a=setTimeout(b,function(t){var r=e-(t-u);return h?L(r,i-(t-l)):r}(t))}function w(t){return a=void 0,p&&o?g(t):(o=n=void 0,c)}function y(){var t=d(),r=v(t);if(o=arguments,n=this,u=t,r){if(void 0===a)return function(t){return l=t,a=setTimeout(b,e),f?g(t):c}(u);if(h)return clearTimeout(a),a=setTimeout(b,e),g(u)}return void 0===a&&(a=setTimeout(b,e)),c}return e=P(e)||0,s(r)&&(f=!!r.leading,i=(h="maxWait"in r)?V(P(r.maxWait)||0,e):i,p="trailing"in r?!!r.trailing:p),y.cancel=function(){void 0!==a&&clearTimeout(a),l=0,o=u=n=a=void 0},y.flush=function(){return void 0===a?c:w(d())},y};const A=function(t,e,r){var o=!0,n=!0;if("function"!=typeof t)throw new TypeError("Expected a function");return s(r)&&(o="leading"in r?!!r.leading:o,n="trailing"in r?!!r.trailing:n),R(t,e,{leading:o,maxWait:e,trailing:n})};const M=function(t,e){return function(r){return t(e(r))}}(Object.getPrototypeOf,Object);var I=Function.prototype,K=Object.prototype,$=I.toString,k=K.hasOwnProperty,U=$.call(Object);const D=function(t){if(!T(t)||"[object Object]"!=O(t))return!1;var e=M(t);if(null===e)return!0;var r=k.call(e,"constructor")&&e.constructor;return"function"==typeof r&&r instanceof r&&$.call(r)==U};const F=function(t){return T(t)&&1===t.nodeType&&!D(t)};class z extends t.Plugin{constructor(t){super(t),this.set("characters",0),this.set("words",0),Object.defineProperties(this,{characters:{get(){return this.characters=this._getCharacters(this._getText())}},words:{get(){return this.words=this._getWords(this._getText())}}}),this.set("_wordsLabel",void 0),this.set("_charactersLabel",void 0),this._config=t.config.get("wordCount")||{},this._outputView=void 0,this._wordsMatchRegExp=n.env.features.isRegExpUnicodePropertySupported?new RegExp("([\\p{L}\\p{N}]+\\S?)+","gu"):/([a-zA-Z0-9À-ž]+\S?)+/gu}static get pluginName(){return"WordCount"}init(){this.editor.model.document.on("change:data",A(this._refreshStats.bind(this),250)),"function"==typeof this._config.onUpdate&&this.on("update",((t,e)=>{this._config.onUpdate(e)})),F(this._config.container)&&this._config.container.appendChild(this.wordCountContainer)}destroy(){this._outputView&&(this._outputView.element.remove(),this._outputView.destroy()),super.destroy()}get wordCountContainer(){const t=this.editor,r=t.t,o=t.config.get("wordCount.displayWords"),n=t.config.get("wordCount.displayCharacters"),i=e.Template.bind(this,this),s=[];return this._outputView||(this._outputView=new e.View,(o||void 0===o)&&(this.bind("_wordsLabel").to(this,"words",(t=>r("Words: %0",t))),s.push({tag:"div",children:[{text:[i.to("_wordsLabel")]}],attributes:{class:"ck-word-count__words"}})),(n||void 0===n)&&(this.bind("_charactersLabel").to(this,"characters",(t=>r("Characters: %0",t))),s.push({tag:"div",children:[{text:[i.to("_charactersLabel")]}],attributes:{class:"ck-word-count__characters"}})),this._outputView.setTemplate({tag:"div",attributes:{class:["ck","ck-word-count"]},children:s}),this._outputView.render()),this._outputView.element}_getText(){let t="";for(const e of this.editor.model.document.getRoots())""!==t&&(t+="\n"),t+=i(e);return t}_getCharacters(t){return t.replace(/\n/g,"").length}_getWords(t){return(t.match(this._wordsMatchRegExp)||[]).length}_refreshStats(){const t=this._getText(),e=this.words=this._getWords(t),r=this.characters=this._getCharacters(t);this.fire("update",{words:e,characters:r})}}})(),(window.CKEditor5=window.CKEditor5||{}).wordCount=o})();