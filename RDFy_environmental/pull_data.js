var util = require("util"),
    request = require("request"),
	fs = require("fs"),
    base_url = null,
    host = "dashboard.us.enableiot.com",
    api_root = "/v1/api",
    g_username = "",
    g_password = "",
    g_account_name = "test",
    g_device_id = "adummy-lab",
    //g_comp_type = "light.v1.0",
    //g_comp_name = "light",
	cid = "cdf50a25-b857-43ff-a0c5-75bf9c8b6fc5";

    base_url = util.format("https://%s%s", host,api_root);
    //var device_name= util.format("Device-%s", g_device_id);


var main=function(){
    
    var token;
    var user_id;
    var ac_id;
    
    get_token(g_username,g_password, function(CBtoken){
        
        token=CBtoken;
        
        get_user_id(CBtoken, function(CBid){
            
                user_id=CBid;
            
                get_account_id(CBid,g_account_name,CBtoken, function(CBaccount){
                    
                    ac_id=CBaccount;
                    
                    get_observation(ac_id,g_device_id,cid,-300,token, function(data_set){
                                    
                                    print_observation_counts(data_set);
                    });
                    
                });
        });
        
    } );
    
    
};

//var callback = function(err){ if (err) throw err; };


var get_token= function(username, password, MyCallBack){
    
    var url = util.format("%s/auth/token",base_url);
    var payload = {"username": username, "password": password};
    var token;
    
    make_request(make_options(url, "POST", payload), 
            function(err, data){
                    if (err) MyCallBack(err);
                    if (data) {
                                token = data.token;
								console.log("Token: " + token);
                                return MyCallBack(token);
                    }
            });
};

var get_user_id=function(token_t, MyCallBack){
    var url = util.format("%s/auth/tokenInfo",base_url);
    var user_id;
    var payload={};
    
    make_request(make_options(url, "GET", payload,token_t), 
            function(err, data){
                    if (err) MyCallBack(err);
                    if (data) {
                            user_id = data.payload.sub;
                            console.log("User Id: " + user_id);
							return MyCallBack(user_id);
                    }
            });

};

var get_account_id=function(user_id,account_name,token_t,MyCallBack){
    
    var account_id;
    var url = util.format("%s/users/%s",base_url,user_id);
    make_request(make_options(url, "GET", null, token_t), 
            function(err, data){
                    if (err) MyCallBack(err);
                    if (data) {
							parse_account_id(data.accounts,account_name, function(account_id){
							console.log("Account Id:"+account_id);
							return MyCallBack(account_id);
						});
                    }
            });
};

var parse_account_id = function(obj,acn,MyCallBack){
  var result = null;
  Object.keys(obj).forEach(function(account_id) {
    var account_args = obj[account_id];
    Object.keys(account_args).forEach(function(arg) {
      var arg_val = account_args[arg];
      if (arg == "name" && arg_val == acn){
        //console.log("2. Account Id:"+account_id);  
        result = account_id;
		return MyCallBack(result);
      }
    });
  });
};

var get_observation=function(account_id, devic_id, component_id,period,token_t, MyCallBack){
    
    var url = util.format("%s/accounts/%s/data/search",base_url,account_id);
    //var dataset;
    var search = {
        "from": period,
        "targetFilter": {
            "deviceList": [g_device_id]
        },
        "metrics": [
            {
                "id": component_id
            }
        ]
    };
    
	make_request(make_options(url, "POST", search, token_t), 
        function(err, data){
                if (err) MyCallBack(err);
                if (data) {
                        //dataset = data.series;
                        //return MyCallBack(data);
						return MyCallBack(JSON.stringify(data));
                        //console.log("Data: " + dataset);
                }
        });
};


var print_observation_counts = function(obj){
	
	console.log("1: "+obj);
	
};
	
///////////////////MAKE OPTIONS

var make_options = function(url, method, data, token){
  var options = {
    "url": url,
    "proxy": null,
    "method": method,
    "json": true,
    "followAllRedirects": true,
    "strictSSL": false,
    "body": data || {},
    "headers": {}
  }
  if (process.env.PROXY) {
    // logger.debug("Proxy: %s", process.env.PROXY);
    options.proxy = process.env.PROXY;
    options.strictSSL = false;
  }
  if (token) options.headers = { "Authorization": "Bearer " + token };
  return options;
}

var process_response = function(res, body, callback) {
    var data = null;
    if (res.statusCode === 200 || res.statusCode === 201) {
        if (res.headers['content-type'] &&
            res.headers['content-type'].indexOf('application/json') > -1) {
            data = body;
        } else {
            data = null;
        }
    } else if (res.statusCode === 204) {
        data = { status: "Done" };
    }
    return  callback(data);
}

var make_request = function(options, callback){
  request(options, function (error, response, body) {
    if (!error && (response.statusCode === 200 ||
                   response.statusCode === 201 ||
                   response.statusCode === 204)) {
        process_response(response, body, function(json_data) {
             return callback(null, json_data);
        });
    } else {
        error = error || body;
        return callback(error);
    }
  });
};


///////////////////////////////////////

main();