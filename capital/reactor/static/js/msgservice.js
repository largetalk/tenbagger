/*
  create by lu hongming
  2013-07-04
*/

msgservice = {
  messenger: null,
  init: function(){
    var me = this;
    this.messenger = Messenger.initInIframe();
    this.messenger.onmessage = function(data){
      if(!!data && data != '')
        msgservice.message_parse(JSON.parse(data));
    };

    //初始化完整，给父窗口发一个通知
    msgservice.messenger.send(JSON.stringify({'state': 'complete'}));
  },
  _send_callback: function(data, type, callback_id){
    if(!!callback_id){
      var rv = {
        data: data,
        type: type,
        callback_id: callback_id
      };

      msgservice.messenger.send(JSON.stringify(rv));
    }
  },
  _get_json: function(url, prams, callback_id) {
    jQuery.support.cors = true; 
    $.ajax(url, {
      "type": "GET",
      "data": prams,
      "dataType": "json",
      "cache": false,
      "success": function(data, status, xhr) {
        msgservice._send_callback(data, 'success', callback_id);
      },
      "error": function(xhr, status) {
        msgservice._send_callback({xhr: xhr, status: status}, 'error', callback_id);
      }
    });
  },
  _post_json: function(url, prams, callback_id) {
    jQuery.support.cors = true; 
    $.ajax(url, {
      "data": {
        response: JSON.stringify(prams)
      },
      "type": 'POST',
      "dataType": "json",
      "crossDomain": true,
      "cache": false,
      "success": function(data) {
        msgservice._send_callback(data, 'success', callback_id);
      },
      "error": function(xhr, status) {
        msgservice._send_callback({xhr: xhr, status: status}, 'error', callback_id);
      }
    });
  },

  message_parse: function(message){
    if(!message || message == '')
      return;

    var json = message;

    var fun = msgservice[{'get': '_get_json', 'post': '_post_json'}[json.type]];

    //msgservice._send_callback(json.data, 'success', json.callback_id);

    if(!!fun)
      fun(json.url, json.data, json.callback_id);
  }
};