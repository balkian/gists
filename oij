SELECT count(*) AS C, payload->'retweeted_status'->>'id' AS cat, payload->'retweeted_status'->>'text' AS Tweet FROM messages WHERE jsonb_typeof(payload) = 'object' and payload->>'text' not like '%http%' GROUP BY cat, Tweet ORDER BY C DESC;
# Works just fine


SELECT count(*) AS C, payload->'retweeted_status'->>'id' AS cat, payload->'retweeted_status'->>'text' AS Tweet, payload->'retweeted_status'->'User'->>'screen_name' AS User FROM messages WHERE jsonb_typeof(payload) = 'object' and payload->>'text' not like '%http%' GROUP BY cat, Tweet, User ORDER BY C DESC;
# Doesn't work
# ------------
# ERROR:  column "messages.payload" must appear in the GROUP BY clause or be used in an aggregate function
# LINE 1: ...t, payload->'retweeted_status'->>'text' AS Tweet, payload->'...

#Problem: User was the name of a column :)
