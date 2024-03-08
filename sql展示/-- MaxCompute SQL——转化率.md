-- MaxCompute SQL 

-- ********************************************************************--

-- author:zwq01668202

-- create time:2023-04-19 15:34:00

-- ********************************************************************--

 



-----uv转化率

----web端

--数据准备

DROP TABLE if EXISTS tdl_anticheating_item_exposure;

CREATE TABLE if not EXISTS tdl_anticheating_item_exposure  -----web端存在pv但是有买家和无买家数据的情况

LIFECYCLE 7 as 

SELECT b.seller_admin_id,item_id,log_time,buyer_admin_id 

 from 

 (

  select seller_admin_id,item_id,log_time,buyer_admin_id from ae_cdm.dwd_ae_log_web_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

  where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 365

  and buyer_admin_id is NOT NULL 

 ) a

 JOIN 

 (

  SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

  WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

  GROUP BY product_id,seller_admin_id

 ) b  

on a.item_id = b.product_id

GROUP BY b.seller_admin_id,item_id,log_time,buyer_admin_id-----web 端登录用户曝光表

 

 

UNION ALL 

 

 

SELECT b.seller_admin_id,item_id,log_time,buyer_admin_id 

 from 

 (

  select seller_admin_id,item_id,log_time,buyer_admin_id from ae_cdm.dwd_ae_log_web_item_lead_di-----不需要去重

  where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 365

  and buyer_admin_id is null 

 ) a

 JOIN 

 (

  SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

  WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

  GROUP BY product_id,seller_admin_id

 ) b  

on a.item_id = b.product_id------web 端 非登录用户曝光表

;

 

 

 

---web 端曝光

 

 

DROP TABLE if EXISTS tdl_anticheating_item_exposure_total;

CREATE TABLE if not EXISTS tdl_anticheating_item_exposure_total  -----web端存在pv但是有买家和无买家数据的情况

LIFECYCLE 7 as

SELECT 

seller_admin_id,

item_id,

substring(log_time,1,10) as pv_day,

count(1) as pv_num,

count(DISTINCT buyer_admin_id) exposure_total_person,

COUNT(buyer_admin_id) uv,

COUNT(1)-count(buyer_admin_id) as exposure_total_unlogin  -----可能未登录的买家，商品在每天的曝光量(曝光量为0的为无登录用户)

 from 

 tdl_anticheating_item_exposure 

GROUP BY seller_admin_id,item_id,pv_day

;

 

----下单成功

DROP TABLE if EXISTS tdl_anticheating_item_order_success_coupon;

CREATE TABLE if not EXISTS tdl_anticheating_item_order_success_coupon

LIFECYCLE 7 as

Select 

sel_ad_id,

item_id,

substring(log_time,1,10) as pv_day,

count(distinct t1.parent_order_id) as order_num_peritem,

COUNT(DISTINCT t1.buyer_admin_id) as person_num_peritem

From

 (

  SELECT b.seller_admin_id as sel_ad_id,item_id,log_time,buyer_admin_id,parent_order_id

  from 

  (

   select seller_admin_id,item_id,log_time,buyer_admin_id,parent_order_id from ae_cdm.dwd_ae_log_web_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

   where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 365

  ) a

  JOIN 

  (

   SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

   WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

   GROUP BY product_id,seller_admin_id

  ) b  

  on a.item_id = b.product_id

  GROUP BY b.seller_admin_id,item_id,log_time,buyer_admin_id,parent_order_id-----web 端曝光表

 ) t1 -----每日曝光表

Join 

(

 Select 

 buyer_admin_id,

 gmt_create,

 parent_order_id

 from sec_intlcdm.dwd_ae_trd_ord_df

 where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

 and parent_order_id is not null

 and platform in ('msite','pc_www')

 and total_mj_coupon_fee > 0

 AND plfm_coupon_id is not null

) t2 ------下单成功表

On t1.parent_order_id = t2.parent_order_id 

Group by sel_ad_id,item_id,pv_day;

  

 

 

 

-------web支付成功表

DROP TABLE if EXISTS tdl_anticheating_item_payment_success_coupon;

CREATE TABLE if not EXISTS tdl_anticheating_item_payment_success_coupon

LIFECYCLE 7 AS 

SELECT 

sel_ad_id,

item_id,

substring(log_time,1,10) pv_day,

count(distinct t1.parent_order_id ) as payment_num_peritem,

COUNT(DISTINCT t1.buyer_admin_id) as person_payment_num_peritem

FROM 

(

 SELECT b.seller_admin_id as sel_ad_id,item_id,log_time,buyer_admin_id,parent_order_id

 from 

 (

  select seller_admin_id,item_id,log_time,buyer_admin_id,parent_order_id from ae_cdm.dwd_ae_log_web_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

  where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 365

 ) a

 JOIN 

 (

  SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

  WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

  GROUP BY product_id,seller_admin_id

 ) b  

 on a.item_id = b.product_id

 GROUP BY b.seller_admin_id,item_id,log_time,buyer_admin_id,parent_order_id-----web 端曝光表

) t1

Join 

(

 Select 

 buyer_admin_id,

 gmt_create,

 parent_order_id,

 gmt_pay

 from sec_intlcdm.dwd_ae_trd_ord_df a

 where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

 and gmt_pay is not null

 and gmt_refund_create is null

 and platform in ('msite','pc_www')

 and total_mj_coupon_fee > 0

 and plfm_coupon_id is not null

 GROUP BY buyer_admin_id,gmt_create,parent_order_id,gmt_pay

) t2 ------支付成功表

On t1.parent_order_id = t2.parent_order_id 

GROUP BY 

sel_ad_id,item_id,pv_day

;

 

 

DROP TABLE if EXISTS tdl_anticheating_item_web_overall_coupon;

CREATE TABLE if not EXISTS tdl_anticheating_item_web_overall_coupon

LIFECYCLE 7 AS 

SELECT 

a.seller_admin_id,

a.item_id,

a.pv_day,

pv_num,

uv,

exposure_total_person,

exposure_total_unlogin,

order_num_peritem,

person_num_peritem,

person_payment_num_peritem,

payment_num_peritem 

FROM tdl_anticheating_item_exposure_total a 

 

left OUTER JOIN tdl_anticheating_item_order_success_coupon C 

on a.seller_admin_id = c.sel_ad_id

and a.item_id = c.item_id

and a.pv_day = c.pv_day

left OUTER JOIN tdl_anticheating_item_payment_success_coupon d

on a.seller_admin_id = d.sel_ad_id

and a.item_id = d.item_id

and a.pv_day = d.pv_day

;

 

---app端

 

DROP TABLE if EXISTS tdl_anticheating_item_app_exposure;

CREATE TABLE if not EXISTS tdl_anticheating_item_app_exposure  -----web端存在pv但是有买家和无买家数据的情况

LIFECYCLE 7 as 

SELECT b.seller_admin_id,item_id,log_time,member_id

 from 

 (

   select seller_admin_id,item_id,log_time,member_id from ae_cdm.dwd_ae_log_app_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 180

and member_id is NOT NULL 

and member_id <> '-'

) a

 JOIN 

 (

   SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

GROUP BY product_id,seller_admin_id

) b  

on a.item_id = b.product_id

GROUP BY b.seller_admin_id,item_id,log_time,member_id----app 端登录用户曝光表

 

UNION ALL 

 

SELECT b.seller_admin_id,item_id,log_time,member_id

 from 

 (

   select seller_admin_id,item_id,log_time,member_id from ae_cdm.dwd_ae_log_app_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 180

and member_id = '-'

) a

 JOIN 

 (

   SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

GROUP BY product_id,seller_admin_id

) b  

on a.item_id = b.product_id------web 端 非登录用户曝光表

 

;

 

DROP TABLE if EXISTS tdl_anticheating_item_app_exposure_total;

CREATE TABLE if not EXISTS tdl_anticheating_item_app_exposure_total  -----app端存在pv但是有买家和无买家数据的情况

LIFECYCLE 7 as

SELECT 

seller_admin_id,

item_id,

substring(log_time,1,10) as pv_day,

count(1) as pv_num,

count(DISTINCT member_id) exposure_total_person,

COUNT(member_id) uv,

COUNT(1)-count(member_id) as exposure_total_unlogin  -----可能未登录的买家，商品在每天的曝光量(曝光量为0的为无登录用户)

 from 

 tdl_anticheating_item_app_exposure 

GROUP BY seller_admin_id,item_id,pv_day

;

 

----下单成功

DROP TABLE if EXISTS tdl_anticheating_item_app_order_success_coupon;

CREATE TABLE if not EXISTS tdl_anticheating_item_app_order_success_coupon

LIFECYCLE 7 as

Select 

sel_ad_id,

item_id,

substring(gmt_create,1,10) as create_day,

count(distinct t1.parent_order_id) as order_num_peritem,

COUNT(DISTINCT t1.member_id) as person_num_peritem

From

 (

   SELECT b.seller_admin_id as sel_ad_id,item_id,log_time,member_id,parent_order_id

 from 

 (

   select seller_admin_id,item_id,log_time,member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 180

) a

 JOIN 

 (

   SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

GROUP BY product_id,seller_admin_id

) b  

on a.item_id = b.product_id

GROUP BY b.seller_admin_id,item_id,log_time,member_id,parent_order_id-----web 端曝光表

) t1 -----每日曝光表

Join 

(

Select 

buyer_admin_id,

gmt_create,

parent_order_id

from sec_intlcdm.dwd_ae_trd_ord_df

where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

and parent_order_id is not null

and platform in ('vk_mini_app','android','wl_www','iphone','ipad')

and total_mj_coupon_fee > 0

AND plfm_coupon_id is not null

) t2 ------下单成功表

On t1.parent_order_id = t2.parent_order_id 

Group by sel_ad_id,item_id,create_day;

  

 

-----app端支付成功表

DROP TABLE if EXISTS tdl_anticheating_item_app_payment_success_app;

CREATE TABLE if not EXISTS tdl_anticheating_item_app_payment_success_app

LIFECYCLE 7 AS 

SELECT 

sel_ad_id,

item_id,

substring(log_time,1,10) pv_day,

count(distinct t1.parent_order_id ) as payment_num_peritem,

COUNT(DISTINCT t1.member_id) as person_payment_num_peritem

FROM 

(

   SELECT b.seller_admin_id as sel_ad_id,item_id,log_time,member_id,parent_order_id

 from 

 (

   select seller_admin_id,item_id,log_time,member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di-----这里如果没有去重，就会出现买家一次pv,但是多次创建订单,导致pv量统计出错。所以问题买家通过批量订单来套现，导致转化率低。

where datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 180

) a

 JOIN 

 (

   SELECT product_id,seller_admin_id from sec_intlcdm.dwd_ae_trd_ord_df

WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')   

GROUP BY product_id,seller_admin_id

) b  

on a.item_id = b.product_id

GROUP BY b.seller_admin_id,item_id,log_time,member_id,parent_order_id-----web 端曝光表

) t1

Join 

(

Select 

buyer_admin_id,

gmt_create,

parent_order_id,

gmt_pay

from sec_intlcdm.dwd_ae_trd_ord_df a

where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

and gmt_pay is not null

and gmt_refund_create is null

and platform in ('vk_mini_app','android','wl_www','iphone','ipad')

and total_mj_coupon_fee > 0

and plfm_coupon_id is not null

GROUP BY buyer_admin_id,gmt_create,parent_order_id,gmt_pay

) t2 ------支付成功表

On t1.parent_order_id = t2.parent_order_id 

GROUP BY 

sel_ad_id,item_id,pv_day

;

 

----app端汇总

DROP TABLE if EXISTS tdl_anticheating_item_app_app_overall;

CREATE TABLE if not EXISTS tdl_anticheating_item_app_app_overall

LIFECYCLE 7 AS 

SELECT 

a.seller_admin_id,

a.item_id,

a.pv_day,

exposure_total_person,

pv_num,

order_num_peritem,

payment_num_peritem 

FROM tdl_anticheating_item_app_exposure_total a 

left OUTER JOIN tdl_anticheating_item_app_order_success_coupon C 

on a.seller_admin_id = c.sel_ad_id

and a.item_id = c.item_id

and a.pv_day = c.create_day

left OUTER JOIN tdl_anticheating_item_app_payment_success_app d

on a.seller_admin_id = d.sel_ad_id

and a.item_id = d.item_id

and a.pv_day = d.pv_day

;

 