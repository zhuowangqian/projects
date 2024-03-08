-- MaxCompute SQL 

-- ********************************************************************--

-- author:zwq01668202

-- create time:2023-04-27 16:22:33

-- ********************************************************************--

 

 

---web 端

-- -捞出所有无pv的买家和卖家数据

-- -即用券下单且无pv数据

 

 

 

 ----零pv商家

DROP TABLE if EXISTS tdl_anticheating_zeroPV_lists;

CREATE TABLE if NOT EXISTS tdl_anticheating_zeroPV_lists

LIFECYCLE 7 AS 

SELECT

 seller_admin_id,sum(order_num) order_total_num

FROM

 (

  Select 

  a.seller_admin_id,

  a.buyer_admin_id as a_byr,

  b.buyer_admin_id as b_byr,

  COUNT(DISTINCT a.parent_order_id) order_num

  from sec_intlcdm.dwd_ae_trd_ord_df a

  left OUTER JOIN 

  (

   select buyer_admin_id,parent_order_id from ae_cdm.dwd_ae_log_web_item_lead_di

   where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') <= 365

   and datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 370

   and buyer_admin_id is not null

   and parent_order_id is not null ----有pv记录且下单的买家

   GROUP BY buyer_admin_id,parent_order_id

  ) b

  -- on a.buyer_admin_id = b.buyer_admin_id

  on a.parent_order_id = b.parent_order_id

  where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

  and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 180

  and gmt_pay is NOT NULL 

  and gmt_refund_create is null

  and platform in ('msite','pc_www')

  and total_mj_coupon_fee > 0

  and plfm_coupon_id is not null

  AND   a.buyer_admin_id NOT IN (

   SELECT buyer_admin_id

   FROM  sec_aeapp.adm_ae_byr_dropshipper_d

  ) 

  GROUP BY a.seller_admin_id,a.buyer_admin_id,b.buyer_admin_id

 ) t1

WHERE b_byr is null

GROUP BY seller_admin_id

UNION 

SELECT

 seller_admin_id,sum(order_num) order_total_num

FROM

 (

  Select 

  a.seller_admin_id,

  a.buyer_admin_id as a_byr,

  b.buyer_admin_id as b_byr,

  COUNT(DISTINCT a.parent_order_id) order_num

  from sec_intlcdm.dwd_ae_trd_ord_df a

  left OUTER JOIN 

  (

   select buyer_admin_id,parent_order_id from ae_cdm.dwd_ae_log_web_item_lead_di

   where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') <= 545

   and datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') > 180

   and datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 550

   and datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') > 175

   and buyer_admin_id is not null

   and parent_order_id is not null ----有pv记录且下单的买家

   GROUP BY buyer_admin_id,parent_order_id

  ) b

  -- on a.buyer_admin_id = b.buyer_admin_id

  on a.parent_order_id = b.parent_order_id

  where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

  and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') > 180

  and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

  and gmt_pay is NOT NULL 

  and gmt_refund_create is null

  and platform in ('msite','pc_www')

  and total_mj_coupon_fee > 0

  and plfm_coupon_id is not null

  AND   a.buyer_admin_id NOT IN (

   SELECT buyer_admin_id

   FROM  sec_aeapp.adm_ae_byr_dropshipper_d

  ) 

  GROUP BY a.seller_admin_id,a.buyer_admin_id,b.buyer_admin_id

 ) t1

WHERE b_byr is null

GROUP BY seller_admin_id

;

 

 

---zero_pv 买家名单

DROP TABLE if EXISTS tdl_anticheating_zeroPV_byr_lists;

CREATE TABLE if NOT EXISTS tdl_anticheating_zeroPV_byr_lists

LIFECYCLE 7 AS 

SELECT

 a_byr,SUM(order_num) order_total_num

FROM

 (

  Select 

  a.seller_admin_id,

  a.buyer_admin_id as a_byr,

  b.buyer_admin_id as b_byr,

  COUNT(DISTINCT a.parent_order_id) order_num

  from sec_intlcdm.dwd_ae_trd_ord_df a

  left OUTER JOIN 

  (

   select buyer_admin_id,parent_order_id from ae_cdm.dwd_ae_log_web_item_lead_di

   where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') <= 365

   and datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 370

   and buyer_admin_id is not null

   and parent_order_id is not null ----有pv记录且下单的买家

   GROUP BY buyer_admin_id,parent_order_id

  ) b

  -- on a.buyer_admin_id = b.buyer_admin_id -----用买家id进行连接是为了判断买家下单期间没有访问数据

  on a.parent_order_id = b.parent_order_id  ------用订单id进行连接，能够证明一批订单是无访问下单的，同时也证明了买家也是无访问的，就无需考虑时间，但是可能会误伤到一批购物车跳转的买家，假设一个买家1个月前访问商品并加购物车，pv表里只有买家访问记录，没有订单记录，然后购物车直接下单，pv表里没有访问记录。

  where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

  and gmt_pay is NOT NULL 

  and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 180

  and gmt_refund_create is null

  and platform in ('msite','pc_www')

  and total_mj_coupon_fee > 0

  and plfm_coupon_id is not null

  GROUP BY a.seller_admin_id,a.buyer_admin_id,b.buyer_admin_id

 ) t1

WHERE b_byr is null

GROUP BY a_byr

UNION 

SELECT

 a_byr,SUM(order_num) order_total_num

FROM

 (

  Select 

  a.seller_admin_id,

  a.buyer_admin_id as a_byr,

  b.buyer_admin_id as b_byr,

  COUNT(DISTINCT a.parent_order_id) order_num

  from sec_intlcdm.dwd_ae_trd_ord_df a

  left OUTER JOIN 

  (

   select buyer_admin_id,parent_order_id from ae_cdm.dwd_ae_log_web_item_lead_di

   where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') <= 545

   AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') > 180

   and datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') > 175

   and datediff(GETDATE(),TO_DATE(ds,'yyyymmdd'),'dd') <= 550

   and buyer_admin_id is not null

   and parent_order_id is not null ----有pv记录且下单的买家

   GROUP BY buyer_admin_id,parent_order_id

  ) b

  -- on a.buyer_admin_id = b.buyer_admin_id -----用买家id进行连接是为了判断买家下单期间没有访问数据

  on a.parent_order_id = b.parent_order_id  ------用订单id进行连接，能够证明一批订单是无访问下单的，同时也证明了买家也是无访问的，就无需考虑时间，但是可能会误伤到一批购物车跳转的买家，假设一个买家1个月前访问商品并加购物车，pv表里只有买家访问记录，没有订单记录，然后购物车直接下单，pv表里没有访问记录。

  where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

  and gmt_pay is NOT NULL 

  and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') > 180

  and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

  and gmt_refund_create is null

  and platform in ('msite','pc_www')

  and total_mj_coupon_fee > 0

  and plfm_coupon_id is not null

  GROUP BY a.seller_admin_id,a.buyer_admin_id,b.buyer_admin_id

 ) t1

WHERE b_byr is null

GROUP BY a_byr

;

 

-- -求用券订单中 zero_pv买家占比

DROP TABLE if EXISTS tdl_anticheating_zero_pv_rate;

CREATE TABLE if NOT EXISTS tdl_anticheating_zero_pv_rate

LIFECYCLE 7 as

Select 

seller_admin_id,

round(COUNT(DISTINCT a_byr)/COUNT(DISTINCT buyer_admin_id),3) as zero_pv_rate,

COUNT(distinct a_byr) as zero_pv_byr_num,

COUNT(distinct buyer_admin_id) as total_web_byr_num,

COUNT(DISTINCT parent_order_id) coupon_order_num,

COUNT(distinct IF(a_byr is not null,parent_order_id,null)) zero_pv_order_num,

round(COUNT(DISTINCT IF(a_byr is not null,parent_order_id,null))/COUNT(DISTINCT parent_order_id),3) as zero_pv_order_rate

from sec_intlcdm.dwd_ae_trd_ord_df a

LEFT OUTER JOIN 

(

SELECT a_byr FROM tdl_anticheating_zeroPV_byr_lists

) b

on a.buyer_admin_id = b.a_byr

where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

and gmt_refund_create is null

and platform in ('msite','pc_www')

and total_mj_coupon_fee > 0

and plfm_coupon_id is not null

AND seller_admin_id in

 (

SELECT seller_admin_id FROM tdl_anticheating_zeroPV_lists

 )

GROUP BY seller_admin_id

HAVING coupon_order_num > 20

 

;

 

 

 

----处理app表

DROP TABLE if EXISTS tdl_anticheating_dwd_ae_log_app_item_lead_di_365days;

CREATE TABLE if NOT EXISTS tdl_anticheating_dwd_ae_log_app_item_lead_di_365days

LIFECYCLE 7 AS 

 select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyy-mm-dd'),'dd') <= 100

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 105

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

UNION 

select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') > 100

AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') <= 200

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') > 95

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 205

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

UNION 

select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') > 200

AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') <= 365

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') > 195

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 370

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

 

 

;

 

 

 

 

DROP TABLE if EXISTS tdl_anticheating_dwd_ae_log_app_item_lead_di_2y;

CREATE TABLE if NOT EXISTS tdl_anticheating_dwd_ae_log_app_item_lead_di_2y

LIFECYCLE 7 AS 

select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') > 365

AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') <= 400

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') > 360

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 405

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

UNION 

select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') > 400

AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') <= 500

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') > 395

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 505

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

UNION 

select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') > 500

AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') <= 600

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') > 495

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 605

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

UNION 

select member_id,parent_order_id from ae_cdm.dwd_ae_log_app_item_lead_di

where datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') > 600

AND datediff(GETDATE(),TO_DATE(SUBSTRING (log_time,1,10),'yyyymmdd'),'dd') <= 730

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') > 595

and datediff(GETDATE(),TO_DATE(SUBSTRING(ds,1,10),'yyyymmdd'),'dd') <= 735

and member_id is not null

and parent_order_id is not null ----有pv记录且下单的买家

GROUP BY member_id,parent_order_id

;

 

 

---汇总app端所有访问信息

DROP TABLE if EXISTS tdl_anticheating_ae_log_app_item_lead_di_2years;

CREATE TABLE if NOT EXISTS tdl_anticheating_ae_log_app_item_lead_di_2years

LIFECYCLE 7 as

SELECT * FROM 

tdl_anticheating_dwd_ae_log_app_item_lead_di_365days

UNION 

SELECT * FROM 

tdl_anticheating_dwd_ae_log_app_item_lead_di_2y

;

 

 

 

----零商品pv

-----app

DROP TABLE if EXISTS tdl_anticheating_zeroPV_app_lists;

CREATE TABLE if NOT EXISTS tdl_anticheating_zeroPV_app_lists

LIFECYCLE 7 AS 

SELECT

 seller_admin_id,sum(order_num) order_total_num

FROM

 (

Select 

a.seller_admin_id,

a.buyer_admin_id as a_byr,

b.member_id as b_byr,

COUNT(DISTINCT a.parent_order_id) order_num

from sec_intlcdm.dwd_ae_trd_ord_df a

left OUTER JOIN 

(

  select member_id,parent_order_id from tdl_anticheating_ae_log_app_item_lead_di_2years

 

 

) b

-- on a.parent_order_id = b.parent_order_id

on a.buyer_admin_id = b.member_id

where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

and gmt_pay is not null

and gmt_refund_create is null

and platform in ('vk_mini_app','android','wl_www','iphone','ipad')

and total_mj_coupon_fee > 0

and plfm_coupon_id is not null

AND   a.buyer_admin_id NOT IN (

​            SELECT buyer_admin_id

​            FROM  sec_aeapp.adm_ae_byr_dropshipper_d

​          ) 

GROUP BY a.seller_admin_id,a.buyer_admin_id,b.member_id

) t1

WHERE b_byr is null

GROUP BY seller_admin_id

 

 

;

 

 

-----zero_pv 买家名单

DROP TABLE if EXISTS tdl_anticheating_zeroPV_byr_app_lists;

CREATE TABLE if NOT EXISTS tdl_anticheating_zeroPV_byr_app_lists

LIFECYCLE 7 AS 

SELECT

 a_byr,SUM(order_num) order_total_num

FROM

 (

Select 

a.seller_admin_id,

a.buyer_admin_id as a_byr,

b.member_id as b_byr,

COUNT(DISTINCT a.parent_order_id) order_num

from sec_intlcdm.dwd_ae_trd_ord_df a

left OUTER JOIN 

(

  select member_id,parent_order_id from tdl_anticheating_ae_log_app_item_lead_di_2years

 

 

) b

-- on a.parent_order_id = b.parent_order_id  ---用订单进行连接 可以判断买家在下单的时候是无pv的，但是还需要排除是否通过购物车等行为进行下单

on a.buyer_admin_id = b.member_id

where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')----如果用买家相互连接，可以判断买家在一定时间内都是无pv的，但是可能在最早的时间处，买家是通过购物车等方式进行连接

and gmt_pay is not null

and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

and gmt_refund_create is null

and platform in ('vk_mini_app','android','wl_www','iphone','ipad')

and total_mj_coupon_fee > 0

and plfm_coupon_id is not null

AND   a.buyer_admin_id NOT IN (

​            SELECT buyer_admin_id

​            FROM  sec_aeapp.adm_ae_byr_dropshipper_d

​          ) 

GROUP BY a.seller_admin_id,a.buyer_admin_id,b.member_id

) t1

WHERE b_byr is null

GROUP BY a_byr

-- order by order_total_num DESC 

;

 

 

 

 

 

---求用券订单中 zero_pv买家占比

DROP TABLE if EXISTS tdl_anticheating_zero_pv_app_rate;

CREATE TABLE if NOT EXISTS tdl_anticheating_zero_pv_app_rate

LIFECYCLE 7 as

Select 

seller_admin_id,

-- SUBSTRING (gmt_create,1,10) create_day,

round(COUNT(DISTINCT a_byr)/COUNT(DISTINCT buyer_admin_id),3) as zero_pv_rate,

COUNT(distinct a_byr) as zero_pv_byr_num,

COUNT(distinct buyer_admin_id) as total_web_byr_num,

COUNT(DISTINCT parent_order_id) coupon_order_num,

COUNT(distinct IF(a_byr is not null,parent_order_id,null)) zero_pv_order_num,

round(COUNT(DISTINCT IF(a_byr is not null,parent_order_id,null))/COUNT(DISTINCT parent_order_id),3) as zero_pv_order_rate

from sec_intlcdm.dwd_ae_trd_ord_df a

LEFT OUTER JOIN 

(

SELECT a_byr FROM tdl_anticheating_zeroPV_byr_app_lists

) b

on a.buyer_admin_id = b.a_byr

where ds = max_pt('sec_intlcdm.dwd_ae_trd_ord_df')

and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

and gmt_pay is not null

and gmt_refund_create is null

and platform in ('vk_mini_app','android','wl_www','iphone','ipad')

and total_mj_coupon_fee > 0

and plfm_coupon_id is not null

AND seller_admin_id in

 (

SELECT seller_admin_id FROM tdl_anticheating_zeroPV_app_lists

 )

GROUP BY seller_admin_id

HAVING coupon_order_num > 20

-- ORDER BY zero_pv_rate desc

;

 

------对比web

 

 

DROP TABLE if EXISTS tdl_anticheating_zero_rate_compare_1;

CREATE TABLE if not EXISTS tdl_anticheating_zero_rate_compare_1

LIFECYCLE 7 as

SELECT 

seller_admin_id,

zero_pv_rate,

zero_pv_byr_num,

zero_pv_order_rate,

zero_pv_order_num,

coupon_order_num,

admin_member_id as punished_seller 

FROM 

tdl_anticheating_zero_pv_rate a

LEFT OUTER JOIN

  (

   SELECT admin_member_id 

   FROM tdl_ae_mntr_anticheating_slr_punish_appeal_info_table_daily_update

  WHERE datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 180

  and cashout_punish_ind = 1

--   IN

--   (

-- SELECT seller_admin_id 

-- FROM 

-- tdl_anticheating_zero_pv_rate

-- -- WHERE zero_pv_rate >= 1

--   )

 GROUP BY admin_member_id

 ) b 

 on a.seller_admin_id = admin_member_id

-- WHERE zero_pv_rate >= 1

;

 

 

 

 

 

---对比app

DROP TABLE if EXISTS tdl_anticheating_zero_rate_app_compare_1;

CREATE TABLE if not EXISTS tdl_anticheating_zero_rate_app_compare_1

LIFECYCLE 7 as

SELECT 

seller_admin_id,

zero_pv_rate,

zero_pv_byr_num,

zero_pv_order_rate,

zero_pv_order_num,

coupon_order_num,

admin_member_id as punished_seller 

FROM 

tdl_anticheating_zero_pv_app_rate a

LEFT OUTER JOIN

  (

   SELECT admin_member_id 

   FROM tdl_ae_mntr_anticheating_slr_punish_appeal_info_table_daily_update

  WHERE datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 180

  and cashout_punish_ind=1

 GROUP BY admin_member_id

 ) b 

 on a.seller_admin_id = admin_member_id

-- WHERE zero_pv_rate >= 1

;

 

 

 

 

----对未处罚的名单打标

DROP TABLE if EXISTS tdl_anticheating_unpunished_risk_lists_overall_web;

CREATE TABLE if NOT EXISTS tdl_anticheating_unpunished_risk_lists_overall_web

LIFECYCLE 7 AS 

SELECT *,'web' as platform FROM tdl_anticheating_zero_rate_compare_1

 

 

 

 DROP TABLE if EXISTS tdl_anticheating_unpunished_risk_lists_overall_app;

CREATE TABLE if NOT EXISTS tdl_anticheating_unpunished_risk_lists_overall_app

LIFECYCLE 7 AS 

 SELECT *,'app' as platform FROM tdl_anticheating_zero_rate_app_compare_1

;

 

 

-----合并处理

DROP TABLE if EXISTS tdl_anticheating_unpunished_risk_lists_overall;

CREATE TABLE if NOT EXISTS tdl_anticheating_unpunished_risk_lists_overall

LIFECYCLE 7 as

SELECT 

DISTINCT 

a.sel_id,

a.order_total_num,

a.buyer_total_num,

b.coupon_order_num as coupon_web,

b.zero_pv_rate as zero_pv_rate_web,

b.zero_pv_byr_num as zero_pv_byr_num_web,

b.zero_pv_order_rate as zero_pv_order_rate_web,

b.zero_pv_order_num as zero_pv_order_num_web,

b.platform as pla_web,

b.punished_seller as punished_web,

c.coupon_order_num as coupon_app,

c.zero_pv_rate as zero_pv_rate_app,

c.zero_pv_byr_num as zero_pv_byr_num_app,

c.zero_pv_order_rate as zero_pv_order_rate_app,

c.zero_pv_order_num as zero_pv_order_num_app,

c.platform as pla_app,

c.punished_seller as punished_app,

round((COALESCE( b.zero_pv_byr_num,0)+COALESCE( c.zero_pv_byr_num,0))/a.buyer_total_num,3) as zero_pv_rate_total,

round((COALESCE( b.zero_pv_order_num,0)+COALESCE( c.zero_pv_order_num,0))/a.order_total_num,3) as zero_pv_order_rate_total

 FROM 

(

SELECT seller_admin_id sel_id,COUNT(DISTINCT parent_order_id) as order_total_num,COUNT(DISTINCT buyer_admin_id) as buyer_total_num

from sec_intlcdm.dwd_ae_trd_ord_df 

WHERE ds = MAX_PT ('sec_intlcdm.dwd_ae_trd_ord_df')

and datediff(GETDATE(),TO_DATE(substring(gmt_create,1,10),'yyyy-mm-dd'),'dd') <= 365

and gmt_pay is not NULL 

and gmt_refund_create is null 

and total_mj_coupon_fee > 0

and plfm_coupon_id is not null

GROUP BY seller_admin_id ) a 

left OUTER join tdl_anticheating_unpunished_risk_lists_overall_web b

on a.sel_id = b.seller_admin_id 

LEFT OUTER JOIN tdl_anticheating_unpunished_risk_lists_overall_app c

on a.sel_id = c.seller_admin_id

HAVING zero_pv_rate_web is not null or zero_pv_rate_app is not null

ORDER BY zero_pv_rate_total DESC 

;

 