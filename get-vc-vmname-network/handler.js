"use strict";
var rp = require('request-promise');
var _ = require('lodash')
process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";

module.exports = (content, callback) => {
    var opts = {
        method: 'POST',
        uri: process.env.ENDPOINT + '/rest/com/vmware/cis/session',
        auth: {
            'username': process.env.USER,
            'password': process.env.PASS
        },
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'vmware-use-header-authn': 'test',
            'vmware-api-session-id': 'null',
        },
        json: true
    };
    rp(opts).then((res) => {
        var opts2 = {
            method: 'GET',
            uri: process.env.ENDPOINT + '/rest/vcenter/vm',
            resolveWithFullResponse: true,
            headers: {
                'accept': 'application/json',
                'vmware-api-session-id': res.value
            },
            json: true
        };
        rp(opts2).then((res2) => {
            var vmid = _.find(res2.body.value, function (vmobj) { return vmobj.name == content; }).vm;
            var opts3 = {
                method: 'GET',
                uri: process.env.ENDPOINT + '/rest/vcenter/vm/' + vmid +'/hardware/ethernet',
                resolveWithFullResponse: true,
                headers: {
                    'accept': 'application/json',
                    'vmware-api-session-id': res.value
                },
                json: true
            };
            rp(opts3).then((res3) => {
                callback(null, res3.body.value);
            });
        });
    });
}
