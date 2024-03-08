-- MaxCompute SQL 

-- ********************************************************************--

-- author:zwq01668202

-- create time:2023-05-14 23:37:20

-- ********************************************************************--

 

 

----物流连号

DROP TABLE IF EXISTS tdl_anticheating_bad_relation_sel_lists

;

CREATE TABLE IF NOT EXISTS tdl_anticheating_bad_relation_sel_lists

LIFECYCLE 7 AS

SELECT DISTINCT a.admin_member_id

​    ,a.company_id

​    ,a.member_status

​    ,a.merchant_status

​    ,a.gmt_member_reg

​    ,a.gmt_shop_begin

​    ,company_name as 公司名称

​    ,target_admin_id

​    ,shop_name

​    ,b.member_status AS target_member_status

​    ,b.gmt_shop_begin AS target_shop_begin

​    ,b.gmt_member_reg AS target_member_reg

FROM  sec_aeapp.adl_ae_prvt_mix_sel_tongren_pairs_df a

JOIN  (

 SELECT admin_member_id

 ,shop_name

 ,member_status

 ,gmt_shop_begin

 ,gmt_member_reg

 FROM  sec_intlcdm.dim_ae_sel_feat_basic

 WHERE  ds = MAX_PT('sec_intlcdm.dim_ae_sel_feat_basic')

) b

​    ON   a.target_admin_id = b.admin_member_id

JOIN (SELECT company_name,admin_member_id FROM 

   sec_aeapp.ads_ae_mntr_anticheating_slr_feature_table

   WHERE ds = MAX_PT ('sec_aeapp.ads_ae_mntr_anticheating_slr_feature_table')

   GROUP BY company_name,admin_member_id

   ) c

on a.admin_member_id = c.admin_member_id

;

----关联商家名单

DROP TABLE if EXISTS tdl_anticheating_relate_seller_lists;

CREATE TABLE if not EXISTS tdl_anticheating_relate_seller_lists

LIFECYCLE 7 as

SELECT target_admin_id,min(dnk) as dnk FROM

 (

  SELECT target_admin_id,DENSE_RANK ()OVER (order by admin_member_id ) as dnk FROM 

  tdl_anticheating_bad_relation_sel_lists

  UNION 

  SELECT admin_member_id,DENSE_RANK ()OVER (order by admin_member_id ) as dnk

  FROM tdl_anticheating_bad_relation_sel_lists

 ) t1

GROUP BY target_admin_id

;

 

 

 

----找出物流单号为连号的商家

DROP TABLE IF EXISTS tdl_anticheating_logist_num_is_similar

;

-- SET odps.sql.runtime.flag.executionengine_MaxWindowFunctionBufferSize = 4294967296

-- ;

CREATE TABLE IF NOT EXISTS tdl_anticheating_logist_num_is_similar

LIFECYCLE 7 AS

SELECT seller_admin_id

​    ,parent_order_id

​    ,logist_num

​    ,logist_num - dnk AS logist_dnk

​    ,tag

FROM  (

 SELECT seller_admin_id

 ,parent_order_id

 ,DENSE_RANK() OVER (PARTITION BY tag ORDER BY logist_num ) AS dnk

 ,logist_num

 ,tag

 FROM  (

  SELECT abs(CAST(CONCAT(COALESCE(REGEXP_SUBSTR(logist_num,'[[:digit:]]+',1,1),''),COALESCE(REGEXP_SUBSTR(logist_num,'[[:digit:]]+',1,2),''),COALESCE(REGEXP_SUBSTR(logist_num,'[[:digit:]]+',1,3),''),COALESCE(REGEXP_SUBSTR(logist_num,'[[:digit:]]+',1,4),'')) AS BIGINT)) logist_num

  ,parent_order_id

  ,seller_admin_id

  ,tag

  FROM  (

   SELECT SUBSTRING_INDEX(logist_num,',',-1) AS logist_num

   ,seller_admin_id

   ,parent_order_id

   ,dnk as tag

   FROM  tdl_anticheating_order_detail_info_overview a 

   JOIN tdl_anticheating_relate_seller_lists b 

   on a.seller_admin_id = b.target_admin_id 

   WHERE  logist_num IS NOT NULL

   GROUP BY seller_admin_id

   ,parent_order_id

   ,logist_num

   ,tag

  ) t1

 ) t2

) t3

;

 

DROP TABLE IF EXISTS tdl_anticheating_consecutive_logist_num_sel_lists

;

CREATE TABLE IF NOT EXISTS tdl_anticheating_consecutive_logist_num_sel_lists

LIFECYCLE 7 AS

SELECT seller_admin_id

​    ,logist_dnk

​    ,tag

​    ,COUNT(DISTINCT logist_num) AS logist_quantity

​    ,COUNT(DISTINCT parent_order_id) AS ord_num -- logist_num,

​    -- logist_dnk

FROM  tdl_anticheating_logist_num_is_similar -- WHERE seller_admin_id = 'cn1529194915kbis'

GROUP BY tag

​      ,seller_admin_id

​     ,logist_dnk

ORDER BY logist_quantity DESC

;

 

-- ---验证连号的卖家

DROP TABLE IF EXISTS tdl_anticheating_logist_num_is_similiar_2

;

CREATE TABLE IF NOT EXISTS tdl_anticheating_logist_num_is_similiar_2

LIFECYCLE 7 AS

SELECT seller_admin_id

​    ,a.parent_order_id

​    ,create_day

​    ,a.logist_num

​    ,tag

​    ,logist_dnk

​    ,b.logist_num_real

​    ,b.logist_company

​    ,b.logistics_type

FROM  (

 SELECT seller_admin_id

 ,parent_order_id

 ,logist_num

 ,logist_dnk

 ,tag

 FROM  tdl_anticheating_logist_num_is_similar

 GROUP BY 

 tag,seller_admin_id

 ,parent_order_id

 ,logist_num

 ,logist_dnk

) a

JOIN  (

 SELECT seller_admin_id AS sel_id

 ,parent_order_id

 ,SUBSTRING(gmt_create,1,10) AS create_day

 ,logist_num AS logist_num_real

 ,logist_company

 ,logistics_type

 FROM  tdl_anticheating_order_detail_info_overview

 GROUP BY seller_admin_id

 ,logist_num

 ,logist_company

 ,logistics_type

 ,parent_order_id

 ,create_day

) b

ON   a.parent_order_id = b.parent_order_id

GROUP BY 

​        tag

​      ,seller_admin_id

​     ,a.parent_order_id

​     ,a.logist_num

​     ,logist_dnk

​     ,b.logist_num_real

​     ,b.logist_company

​     ,b.logistics_type

​     ,create_day

;

 

 

 

---查看每个商家下的连号浓度

Drop TABLE if EXISTS tdl_anticheating_consecutive_ord_rate_for_coverage;

CREATE TABLE if NOT EXISTS tdl_anticheating_consecutive_ord_rate_for_coverage

LIFECYCLE 7 as

SELECT 

​     公司名称,

​     tag

​     ,seller_admin_id

​    ,COUNT(DISTINCT parent_order_id) AS ord_num

​    ,SUM(consecutive_sign) AS consecutive_ord_num

​    ,round(SUM(consecutive_sign) / COUNT( DISTINCT parent_order_id),3) AS consecutive_ord_rate

FROM  (

 SELECT DISTINCT tag,a.公司名称,a.seller_admin_id,a.parent_order_id

 ,COALESCE(consecutive_sign,0) AS consecutive_sign

 FROM  tdl_anticheating_consecutive_logist_num_overall a

 LEFT OUTER JOIN (

  SELECT seller_admin_id

  ,logist_dnk

  ,COUNT(DISTINCT parent_order_id) AS ord_num

  ,1 AS consecutive_sign

  FROM  tdl_anticheating_consecutive_logist_num_overall

  GROUP BY seller_admin_id

  ,logist_dnk

  HAVING ord_num > 1

 ) b

 ON   a.logist_dnk = b.logist_dnk

 WHERE  LENGTH(logist_num) >= 5

 AND   LENGTH(logist_num) <= 16

) t1

GROUP BY 

​      tag

​      ,公司名称

​     ,seller_admin_id 

HAVING ord_num > 1

AND   consecutive_ord_num > 1

ORDER BY consecutive_ord_rate DESC,ord_num DESC 

;