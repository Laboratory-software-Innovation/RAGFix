## Here is the code for my stack overflow query for erros that are not compile errors
```
SELECT title,concat('https://stackoverflow.com/questions/',id), tags, score, creationDate From Posts
where body like '%<code>%' and
-- Limiting to Keras Only
tags like '%<pytorch>%' and
(tags like '%<conv-neural-network>%' or
tags like '%<machine-learning>%' or
tags like '%<deep-learning>%' or
tags like '%<deep-learning>%' or
tags like '%<torch>%' or
tags like '%<neural-network>%' or
tags like '%<backpropagation>%' or
tags like '%<linear regression>%' or
tags like '%<linear regression>%') and 
score >=2 and -- Note that the score has been changed from >2 to >=2
(
body not like '%IndexError%' and
body not like '%ValueError%' and
body not like '%TypeError%' and
body not like '%Traceback%' and 
body not like '%ModuleNotFoundError%' and 
body not like '%pip%' and 
body not like '%AssertionError%'and 
body not like '%installation%' 
) 
-- how about run time errors? 
 and
--Limiting to only posts with atleast 1 answer (As a proxy to helps remove questions which are not credible)  
AnswerCount>0 and 
--Limiting to relavent keywords in posts
(body like '%error%' or body like '%bug%' or 
body like '%not work%' or body like '%fail%' or 
body like '%accuracy%' or body like '%expect%' or
body like '%problem%' or body like '%fault%' or
body like '%fix%' or body like '%issue%' or
body like '%loss%' or body like '%activation function%' or
body like '%layer%' or body like '%last layer%' or
body like '%hidden layer%' or body like '%bad performance%' or
body like '%converge%' or body like '%not converge%' or
body like '%nan%' or body like '%advanced activation%' or
body like '%parameter mistakes%' or body like '%incorrect layer%' or
body like '%inaccuracy%' or body like '%loss does not change%' or
body like '%weight does not change%' or body like '%Model does not learn%' or
body like '%wrong%'or body like '%crash%' or body like '%incorrect%'
or body like '%incompatible%'
or body like '%low accuracy%'
or body like '%invalid%'
or body like '%worse%'
or body like '%unexpected%'
or body like '%high loss%'
or body like '%misinterpret%'
or body like '%unknown%'
or body like '%dead relu%'
or body like '%poor weight initialization%'
or body like '%saturated activation%'
or body like '%vanishing gradient%'
or body like '%exploding gradient%'
or body like '%unchanged tensor%'
or body like '%zero%')
```

## Here is the code for my stack overflow search for compile time errors:
```
SELECT title,concat('https://stackoverflow.com/questions/',id), tags, score, creationDate From Posts
where body like '%<code>%' and
-- Limiting to Keras Only
tags like '%<pytorch>%' and
(tags like '%<conv-neural-network>%' or
tags like '%<machine-learning>%' or
tags like '%<deep-learning>%' or
tags like '%<deep-learning>%' or
tags like '%<torch>%' or
tags like '%<neural-network>%' or
tags like '%<backpropagation>%' or
tags like '%<linear regression>%' or
tags like '%<linear regression>%') and 
score >=2 and -- Note that the score has been changed from >2 to >=2
(
body like '%IndexError%' or
body like '%RuntimeError%' or
body like '%ValueError%' or
body like '%TypeError%' or
body like '%Traceback%' or 
body like '%AssertionError%'or 
body like '%installation%' 
) 
-- how about run time errors? 
 and
--Limiting to only posts with atleast 1 answer (As a proxy to helps remove questions which are not credible)  
AnswerCount>0 and 
--Limiting to relavent keywords in posts
(body like '%error%' or body like '%bug%' or 
body like '%not work%' or body like '%fail%' or 
body like '%accuracy%' or body like '%expect%' or
body like '%problem%' or body like '%fault%' or
body like '%fix%' or body like '%issue%' or
body like '%loss%' or body like '%activation function%' or
body like '%layer%' or body like '%last layer%' or
body like '%hidden layer%' or body like '%bad performance%' or
body like '%converge%' or body like '%not converge%' or
body like '%nan%' or body like '%advanced activation%' or
body like '%parameter mistakes%' or body like '%incorrect layer%' or
body like '%inaccuracy%' or body like '%loss does not change%' or
body like '%weight does not change%' or body like '%Model does not learn%' or
body like '%wrong%'or body like '%crash%' or body like '%incorrect%'
or body like '%incompatible%'
or body like '%low accuracy%'
or body like '%invalid%'
or body like '%worse%'
or body like '%unexpected%'
or body like '%high loss%'
or body like '%misinterpret%'
or body like '%unknown%'
or body like '%dead relu%'
or body like '%poor weight initialization%'
or body like '%saturated activation%'
or body like '%vanishing gradient%'
or body like '%exploding gradient%'
or body like '%unchanged tensor%'
or body like '%zero%')
```

Example call: 
python .\chroma_db_code\octo_pack.py --mode 2 --amount 10 --file exp1.csv --load_breaking_examples errors.json