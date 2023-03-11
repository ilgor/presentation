(this.webpackJsonppresentation=this.webpackJsonppresentation||[]).push([[0],{148:function(e,t){},151:function(e,t,n){},152:function(e,t,n){"use strict";n.r(t);var a=n(0),o=n.n(a),r=n(86),l=n.n(r),i=n(15),c=n(16),s=n(18),u=n(17),d=(n(95),n(27)),p=(n(118),function(e){Object(s.a)(n,e);var t=Object(u.a)(n);function n(e,a){var o;return Object(i.a)(this,n),(o=t.call(this,e,a)).state={playerSource:null,videoUrl:null},o}return Object(c.a)(n,[{key:"componentDidMount",value:function(e,t){e!==this.props&&(this.handleValueChange(this.props.videoUrl),this.updatePlayerInfo(this.props.videoUrl),this.player.load()),this.player.play()}},{key:"componentDidUpdate",value:function(e,t){e.videoUrl!==this.props.videoUrl&&(this.handleValueChange(this.props.videoUrl),this.updatePlayerInfo(this.props.videoUrl),this.player.load()),this.player.play()}},{key:"handleValueChange",value:function(e){this.setState({videoUrl:e})}},{key:"updatePlayerInfo",value:function(e){this.setState({playerSource:e})}},{key:"render",value:function(){var e=this;return o.a.createElement("div",{className:"VideoMedia"},o.a.createElement(d.Player,{ref:function(t){e.player=t},videoId:this.props.videoUrl,preload:!0,autoPlay:!0,fluid:!0,playsInline:!0},o.a.createElement(d.ControlBar,{className:"video-react-control-bar-hide",autoHide:!0,disableDefaultControls:!0}),o.a.createElement(d.BigPlayButton,{className:"big-play-button-hide"}," "),o.a.createElement("source",{src:this.state.playerSource})))}}]),n}(a.Component)),m=n(157),v=n(153),f=function(e){Object(s.a)(n,e);var t=Object(u.a)(n);function n(e){return Object(i.a)(this,n),t.call(this,e)}return Object(c.a)(n,[{key:"render",value:function(){return o.a.createElement("div",{className:"MixedMedia"},o.a.createElement(m.a,null,this.props.imageUrl?o.a.createElement(m.a.Title,null,o.a.createElement(v.a,{src:this.props.imageUrl,fluid:!0})):null,this.props.text?o.a.createElement(m.a.Title,null,this.props.text):null))}}]),n}(o.a.Component),h=n(158),g=(o.a.Component,n(89)),y=n.n(g)()({forceNew:!0,transport:["websocket"],transportOptions:{polling:{extraHeaders:{}}}}),E=function(e){Object(s.a)(n,e);var t=Object(u.a)(n);function n(){return Object(i.a)(this,n),t.apply(this,arguments)}return Object(c.a)(n,[{key:"componentDidMount",value:function(){var e=this;y.on("connect",(function(t){console.log("CourseConnection: socket.on('connect') received."),e.setState({client:t,connected:!0})})),y.on("reconnect_attempt",(function(){y.io.opts.transports=["polling","websocket"]})),y.on("message",(function(t){console.log("CourseConnection: socket.on('message') received"),e.props.msgCallbackFromParent(t)})),y.on("event",(function(t){console.log("CourseConnection: socket.on('event') received"),e.setState({event:t}),e.props.eventCallbackFromParent(t)})),y.on("disconnect",(function(t){console.log("CourseConnection: socket.on('disconnect') received"),e.setState({client:t,connected:!1})})),y.on("error",(function(e){console.log(y.id+" error: "+e)})),y.on("connect_error",(function(e){console.log(y.id+" connect error: "+e)})),y.on("connect_timeout",(function(e){console.log(y.id+" client timeout: "+e)}))}},{key:"render",value:function(){return null}}]),n}(o.a.Component),U=(n(85),n(154)),b=n(155),C=n(156),k=function(e){Object(s.a)(n,e);var t=Object(u.a)(n);function n(e){var a,r=this;return Object(i.a)(this,n),(a=t.call(this,e)).readEvents=function(e){var t=e,n={};n.event=e,n.text="text"in t?t.text:null,"videoUrl"in t?null!==n.videoUrl&&(n.videoUrl=t.videoUrl):n.videoUrl=null,n.imageUrl="imageUrl"in t?t.imageUrl:null,a.setState(n)},a.readMessages=function(e){console.log("App received MESSAGE from CourseConnection:"+e);try{document.title=e.split("room_id: ")[1].split(",")[0]}catch(t){document.title="Unknown"}a.setState({message:e})},a.InvalidData=function(e){console.log("Invalid JSON data schema sent from server: "+JSON.stringify(e))},a.EventParser=function(e){if(!("eventType"in e))return o.a.createElement(r.InvalidData,null);switch(e.eventType){case"TextMedia":return"Text";case"VideoMedia":return"Video";case"MixedMedia":return"Image";default:return null}},a.state={message:null,event:null,connected:null,text:null,videoUrl:null,imageUrl:null},a}return Object(c.a)(n,[{key:"render",value:function(){var e;return o.a.createElement("div",{className:"App"},o.a.createElement(E,{msgCallbackFromParent:this.readMessages,eventCallbackFromParent:this.readEvents}),o.a.createElement(C.a,{fluid:!0},(e=this.state).videoUrl&&!e.imageUrl?o.a.createElement(U.a,null,o.a.createElement(b.a,{sm:12},o.a.createElement(p,e))):e.imageUrl&&!e.videoUrl?o.a.createElement(U.a,null,o.a.createElement(b.a,{sm:12},o.a.createElement(f,e))):e.videoUrl&&e.imageUrl?function(e){return[o.a.createElement(U.a,null,o.a.createElement(b.a,{sm:6},o.a.createElement(p,e)),o.a.createElement(b.a,{sm:6},o.a.createElement(f,e)))]}(e):e.videoUrl||e.imageUrl?void 0:o.a.createElement("p",null)))}}]),n}(a.Component);n(151);l.a.render(o.a.createElement(k,null),document.getElementById("root"))},90:function(e,t,n){e.exports=n(152)},95:function(e,t,n){}},[[90,1,2]]]);
//# sourceMappingURL=main.15fb4b87.chunk.js.map