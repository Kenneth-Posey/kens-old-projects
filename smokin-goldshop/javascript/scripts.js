/// <reference path="/jquery.js" />

$(document).ready(function () {

    $('a[class=ajax]').click(function () {
        $this = $(this);
        var tDestination = $this.attr('href');
        var tCustomerId = $this.attr('data-id');
        var tAction = $this.attr('data-action');
        var tVerified = $this.attr('data-verified');
        var tAgentGold = $this.attr('data-agentgold');
        var tInfo = $this.attr('data-info');
        var tEmail = $this.attr('data-email');
        var tNumber = $this.attr('data-number');
        var tOrderNumber = $this.attr('data-orderid');
        var tKey = $this.attr('data-key');
        var tType = $this.attr('data-type');
        
        var tPostData = {};
        tPostData['custid'] = tCustomerId;
        tPostData['Customer'] = tCustomerId;
        tPostData['BlackListType'] = tType;
        tPostData['verified'] = tVerified;
        tPostData['agentgold'] = tAgentGold;
        tPostData['info'] = tInfo;
        tPostData['email'] = tEmail;
        tPostData['phone'] = tNumber;
        tPostData['orderid'] = tOrderNumber;
        tPostData['key'] = tKey;

        $.ajax({
            type: 'post',
            url: tDestination,
            dataType: 'text',
            data: tPostData,
            success: function (data) {
                $this.removeAttr('href');
                $this.text(data);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $this.text(errorThrown);
            }
        });
        return false;
    });

    $('a[class=update]').click(function () {
        $this = $(this);
        var tPostData = {};

        var tOrderNumber = $this.attr('data-orderid');
        tPostData['orderid'] = tOrderNumber;

        var tTextboxSelector = $this.attr('data-textbox');
        tPostData['attribute'] = tTextboxSelector;

        var tTextboxSelectorText = "[id=" + tTextboxSelector + "]";
        var tTextBox = $(tTextboxSelectorText);
        var tValue = tTextBox.value;
        tPostData['value'] = tValue;

        $.ajax({
            type: 'post',
            url: tDestination,
            dataType: 'text',
            data: tPostData,
            success: function (data) {
                $this.removeAttr('href');
                $this.text(data);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $this.text(errorThrown);
            }
        });
        return false;
    });

    $('[id=agentgold]').click(function () {
        $this = $(this);
        var tChecked = $this.prop("checked");

        if (tChecked == true) {
            $('a[class=ajax]').attr("data-agentgold", true);
        }
        else if (tChecked == false) {
            $('a[class=ajax]').attr("data-agentgold", false);
        }
    });

    $('[id=agentgold]').change(function () {
        $this = $(this);
        var tChecked = $this.prop("checked");

        if (tChecked == true) {
            $('a[class=ajax]').attr("data-agentgold", true);
        }
        else if (tChecked == false) {
            $('a[class=ajax]').attr("data-agentgold", false);
        }
    });


    $('a[class=rpcajax]').click(function () {
        $this = $(this);
        var tType = $this.attr('data-type');
        var tCustomerId = $this.attr('data-id');
        
        var tPostData = {};
        tPostData['Customer'] = tCustomerId;
        tPostData['BlackListType'] = tType;
        
        var tDestination = $this.attr('href');

        tPostData = JSON.stringify(tPostData);

        $.ajax({
            type: 'post',
            url: tDestination,
            contentType: 'application/json',
            dataType: 'json',
            data: tPostData,
            success: function (response) {
                $this.text(response.Response);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                $this.text(errorThrown);
            }
        });
        return false;
    });


});
