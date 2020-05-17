function Tracker() {}
//set to true via query string in TIA to debug state call
Tracker.debugMode = myFT.get('debugStateCall') ? true : false;

Tracker.replaceMacros = function(macrosValue, data, queryVar) {
    var macroObj = {
        '[PROTOCOL]':      location.protocol,
        '[DATA]':          encodeURIComponent(data) || 'null',
        '[CACHEBUSTER]':   Math.floor(Math.random() * 9e9),
        '[CACHE_BUSTER]':  Math.floor(Math.random() * 9e9),
        '[CREATIVE_ID]':   myFT.get('creativeID') || '0',
        '[PLACEMENT_ID]':  myFT.get('pID') || myFT.get('ftPlacementID') || '0',
        '[CONFIG_ID]':     myFT.get('confID') || myFT.get('ftConfID') || '0',
        '[IMPRESSION_ID]': myFT.get('impressionID') || '0',
        '[QUERY_VAR]':     queryVar
    };

    for (var macro in macroObj) {
        macrosValue = macrosValue.replace(macro, macroObj[macro]);
    }

    return macrosValue;
};

Tracker.addQueryVarToClickTags = function(queryVar, data, append) {
    data = encodeURIComponent(data);
    for (var i in myFT.placementProperties.clicks) {
        var clickTag = myFT.placementProperties.clicks[i];
        var encodeCount = 0;
        var sbu = ["https://servedby.flashtalking", "http://servedby.flashtalking"];

        if(clickTag.indexOf("servedby.flashtalking") > -1){
            var pub = "",remain = clickTag;

            while(remain.indexOf("https://servedby") === -1 && remain.indexOf("http://servedby") === -1){
                remain = decodeURIComponent(remain);
                encodeCount++;
            }

            if(clickTag.indexOf("servedby.flashtalking")>10){
                for(var pc = 0; pc < sbu.length; pc++){
                    var check = sbu[pc];
                    for(var fe = 0; fe < encodeCount; fe++){
                        check = encodeURIComponent(check);
                    }
                    if(clickTag.indexOf(check)>-1){
                        pub = clickTag.substr(0,clickTag.indexOf(check));
                        remain = remain.substr(remain.indexOf(sbu[pc]));
                    }
                }
            }

            clickTag = pub + remain;
        }
        
        //if query var already exists then we need to replace the value, else just add it in
        var publisherClick = "", ftClick = "";
        if (clickTag.indexOf(queryVar + '=') > -1) {
            if (append) {
                myFT.placementProperties.clicks[i] = clickTag.replace(new RegExp('(' + queryVar + '=(.*?))(&|$)', 'i'), queryVar + '=$2__' + data + '$3');
            }
            else {
                myFT.placementProperties.clicks[i] = clickTag.replace(new RegExp('(' + queryVar + '=(.*?))(&|$)', 'i'), queryVar + '=' + data + '$3');
            }

            if(myFT.placementProperties.clicks[i].indexOf("servedby.flashtalking")>10){
                for(var pc = 0; pc < sbu.length; pc++){
                    if(myFT.placementProperties.clicks[i].indexOf(sbu[pc])>-1){
                        publisherClick = myFT.placementProperties.clicks[i].substr(0,myFT.placementProperties.clicks[i].indexOf(sbu[pc]));
                        ftClick = myFT.placementProperties.clicks[i].substr(myFT.placementProperties.clicks[i].indexOf(sbu[pc]));;
                    }
                }
            }
            else{
                ftClick = myFT.placementProperties.clicks[i];
            }
            for(var count =0; count < encodeCount; count++){
                    ftClick = encodeURIComponent(ftClick);
            }

            myFT.placementProperties.clicks[i] = publisherClick + ftClick;
        }
        else {
            //if impression id query var is found in clickTag then add query var and data, else do nothing
            if (clickTag.indexOf('ft_impID=') > -1) myFT.placementProperties.clicks[i] = clickTag.split('ft_impID=').join(queryVar + '=' + data + '&ft_impID=');
            //if debug mode is enabled then split on query var normally found on TIA clickTags
            if (Tracker.debugMode) {
                myFT.placementProperties.clicks[i] = clickTag.split('n=').join(queryVar + '=' + data + '&n=');
            }

            if(myFT.placementProperties.clicks[i].indexOf("servedby.flashtalking")>10){
                for(var pc = 0; pc < sbu.length; pc++){
                    if(myFT.placementProperties.clicks[i].indexOf(sbu[pc])>-1){
                        publisherClick = myFT.placementProperties.clicks[i].substr(0,myFT.placementProperties.clicks[i].indexOf(sbu[pc]));
                        ftClick = myFT.placementProperties.clicks[i].substr(myFT.placementProperties.clicks[i].indexOf(sbu[pc]));;
                    }
                }
            }
            else{
                ftClick = myFT.placementProperties.clicks[i];
            }
            for(var count =0; count < encodeCount; count++){
                ftClick = encodeURIComponent(ftClick);
            }
            myFT.placementProperties.clicks[i] = publisherClick + ftClick;
        }
    }
};

Tracker.impressionTrackEvent = function(data, queryStringVar) {
    //set default data value
    data = data || 'empty_string';
    //set default query var
    queryStringVar = queryStringVar || 'ft_product';

    //check if function exists already in myFT
    if (!myFT.impressionTrackEvent) {
        //add functions to myFT instance for impression and click tracking
        myFT.impressionTrackEvent = function(data, queryStringVar) {
            var baseStateUrl = '[PROTOCOL]//servedby.flashtalking.com/state/[PLACEMENT_ID];[CREATIVE_ID];[CONFIG_ID];402;[IMPRESSION_ID]/?[QUERY_VAR]=[DATA]&cachebuster=[CACHEBUSTER]';
            //if not debugging, then check for live tag and if impression id, creative id or placement id is not set then do nothing
            var placementId = myFT.get('pID') || myFT.get('ftPlacementID');
            if (!Tracker.debugMode && (!myFT.get('impressionID') || !myFT.get('creativeID') || !placementId)) {
                return;
            }

            //replace macros in the state url
            baseStateUrl = Tracker.replaceMacros(baseStateUrl, data, queryStringVar);
            //fire state call via image object
            (new Image()).src = baseStateUrl;
            //add the query var and value to all clicktags
            Tracker.addQueryVarToClickTags(queryStringVar, data);
        };

        myFT.clickTrackEvent = function(data, queryStringVar, append) {
            //add the query var and value to all clicktags
            Tracker.addQueryVarToClickTags(queryStringVar, data, append);
        };
    }

    //fire only if state call for this query string hasn't been fired previously
    if (!myFT['stateCallFired_' + queryStringVar]) {
        myFT.impressionTrackEvent(data, queryStringVar);
        //add field to myFT to prevent state call from being fired again for this query string var
        myFT['stateCallFired_' + queryStringVar] = true;
    }
};

Tracker.clickTrackEvent = function(data, queryStringVar, append) {
    //set default data value
    data = data || 'empty_string';
    //set default query var
    queryStringVar = queryStringVar || 'ft_product';
    //set default append flag
    append = append || append === null || append === undefined ? true : false;
    //click track event will update all clicktags with data value if it's changed
    myFT.clickTrackEvent(data, queryStringVar, append);
};
