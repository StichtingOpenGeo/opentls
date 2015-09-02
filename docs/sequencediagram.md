Application flow of ov-chipkaart.nl
===================================

![sequence diagram](https://raw.github.com/StichtingOpenGeo/opentls/master/docs/img/sequencediagram.png)

Source for [websequencediagrams.com](https://websequencediagrams.com)

```
title Application flow of ov-chipkaart.nl

app -> oauth2/token: username\npassword\ngrant_type: password\nclient_id: nmOIiEJO5khvtLBK9xad3UkkS8Ua\nclient_secret: FE8ef6bVBiyN0NeyUJ5VOWdelvQa\nscope: openid

oauth2/token -> app: access_token\nid_token\nrefresh_token\ntoken_type: bearer\nscope: openid\nexpires_in: 3300

opt expired
    app -> oauth2/token: refresh_token\ngrant_type: refresh_token\nclient_id: nmOIiEJO5khvtLBK9xad3UkkS8Ua\nclient_secret: FE8ef6bVBiyN0NeyUJ5VOWdelvQa

    oauth2/token -> app: access_token\nid_token\nrefresh_token\ntoken_type: bearer\nscope: openid\nexpires_in: 3300
end

app -> api/authorize: authenticationToken: id_token
api/authorize -> app: o: authorizationToken

app -> cards/list: authorizationToken\nlocale: nl-NL
cards/list -> app: mediumId
loop offset < nextOffset
    app -> transaction/list: authorizationToken\nmediumId\noffset: nextOffset\nlocale: nl-NL
    transaction/list -> app: records[...]\nnextOffset
end
```
