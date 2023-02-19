https://github.com/mxpv/podsync/issues/469#issuecomment-1365453472

Actually my PR is not yet working, but please find a workaround below.

Basically if you find a way to know/get the Channel name, you should be good.

So the idea is to use CURL to query the page using the handle URL, and get the channel ID from the HTML code:

curl -D- --silent https://www.youtube.com/@NASA | tr ',' '\n' | grep "externalId" 
"externalId":"UCLA_DiR1FfKNvjuUpBHmylQ"

Then you can define your feed using the /channel/xxx URL :

[feeds]
  [feeds.NASA]
  url = "https://www.youtube.com/@NASA" # not working
  url = "https://www.youtube.com/channel/UCLA_DiR1FfKNvjuUpBHmylQ" # should be working

