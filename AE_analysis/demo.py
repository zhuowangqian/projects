# coding = utf-8
import crawles
import re
url = 'https://www.aliexpress.us/item/2255800556408778.html'

cookies = {
    'aep_common_f': 'S/MVm6T6yJbDgpwuZLp0+mepUxJIsAcSCB6JXoNYXlM/BGzIEblZbw==',
    '_ga_save': 'yes',
    'cna': 'A0NfHbGscV4CAXWTa0ou3K3W',
    '_gcl_au': '1.1.313344858.1692420089',
    '_ym_uid': '1692420095424565094',
    '_ym_d': '1692420095',
    'x_router_us_f': 'x_alimid=4465986603',
    'xlly_s': '1',
    '_gid': 'GA1.2.26933144.1696743660',
    '_gac_UA-17640202-1': '1.1696743660.CjwKCAjwg4SpBhAKEiwAdyLwvMdAaECMCsHES3QOKMKoNo22ssNIwZh47mSeb7zTCPZmvabeza3GLxoCHugQAvD_BwE',
    '_gcl_aw': 'GCL.1696743660.CjwKCAjwg4SpBhAKEiwAdyLwvMdAaECMCsHES3QOKMKoNo22ssNIwZh47mSeb7zTCPZmvabeza3GLxoCHugQAvD_BwE',
    'xman_us_t': 'x_lid=us2865472608lydae&sign=y&rmb_pp=zhuowangqian0522@gmail.com&x_user=VDk/0qKNGq1XVZR8fHSaKo+ig5n1ewU6iGiRAOR4s6c=&ctoken=i6mzn__ya93w&l_source=aliexpress',
    'xman_f': 'ALEcBxzxOBbggoJtqzCe95ManQNEhTd409SezFjg37h5JGx8Rnzb9A7k0CRPFQ+lEH5ByEbZXszH1SSns68iTLUcYW4wxMm54oDSWpmubLX+PA+7Z4k08C/MRF+u5jNL583DvaycAMbi9oaNtD1db51n2XdW0RmxZPOFE6S0cb2rkzRg56f6HIBunyT4s0XJA7DCdrbhZYd0V6ztE+8PvRY96qeUgf0BAGJzCmZJ9Wg1A3hAT0OFkkabIKSMv63D7hFmLi570rtx8QgeRZihhd13xUn2t1kub8RIR74zfVvue/zfldd969IAEI6+I51fOLik2N8CfVzKLGv+sXKMbQgmAjTXorweVo2W7MlRnWT9zx5RCLzamaXP65csSa2xIC36mXGWiyXxqCO5L1hT+m+wObeIAs3DU4e9qQErdbH/jgxeLonImVwC383r397f',
    'intl_locale': 'en_US',
    'acs_usuc_t': 'x_csrf=dqox7rngq674&acs_rt=85e38da49f4e48a196be029364bf3aa4',
    '_m_h5_tk': 'b88031116432e64915a73c91429ebfa9_1696825157047',
    '_m_h5_tk_enc': '51de8c23a5178363573fd5b77fe38e0e',
    '_ym_isad': '1',
    'XSRF-TOKEN': 'd8dd9a34-1db4-4413-a05f-8b6e3cca4cd7',
    'AKA_A2': 'A',
    'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%093256803817028291%093256804339050988%093256805912708351%092255800491906233%092255800853204202%092255800556408778%093256805906454858%093256805699411481',
    'cto_bundle': 'mRMw418zT3ROck04NkZkUjNiWXZRaUFkQUpkcE9hTWFBQzR6Y3U3VyUyQmlhMXdHTlRPdlRtZ0VPSVpEc2VjWkRnemlnTXJJJTJCU1NtMXdGTFJMNUNybEp5SCUyQiUyQkFRSHhQWXlKSiUyQlEyTkNveHYxZ2wlMkJLU1dQJTJGT1JDN0xnc1I1VHFWcnhHTjMzd3YzSjRvZEtoVWhEJTJGV2V6RHhuc2tVdVprSW9sem9IUjB4aHJvMjVQSmtNJTNE',
    '_m_h5_c': '06731472ba586842c92633e5cca72a0e_1696859396182%3B617cd616338aa29d122107f52a758688',
    '_ga_VED1YSGNC7': 'GS1.1.1696857450.9.0.1696857450.60.0.0',
    '_ga': 'GA1.1.2000821855.1692419935',
    '_ym_visorc': 'b',
    'xman_us_f': 'zero_order=y&x_locale=en_US&x_l=0&x_user=US|wangqian|Zhuo|ifm|4465986603&x_lid=us2865472608lydae&x_c_chg=0&x_c_synced=1&x_as_i=%7B%22aeuCID%22%3A%22adb805cc37ca48488675dba82c1e7d03-1695792061558-07676-UneMJZVf%22%2C%22af%22%3A%22178094261%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cookieCacheEffectTime%22%3A1695897468380%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1695792061558%7D&acs_rt=6837107a988a41f2aeefd19712beff8a',
    'aep_usuc_f': 'site=usa&province=922873780000000000&city=922873786976000000&c_tp=USD&x_alimid=4465986603&isb=y&region=US&b_locale=en_US',
    'tfstk': 'dnL2Sigt8q3VKtD5ci7NzrzGxd_AkwHQSF61sCAGGtX0lrwM4d9kGna15G4wsCIgct_m71vBUtfGjs4uZ1CgmofGIQVlt6eGjF667f7vPna1hxQwsp_ZdvgIRIdAJNDIdH16MIdORU6jR2OvM3XXbi3IM_WY6G2eWPlYCiHH1TYvmBuxRSn49rUvz_DOLIPz5_8PgiBHiEyOQB2OZO16WnygbifRa9GraBQcqGC..',
    'l': 'fBTfACbeN9STy4NDBO5aourza77OEIOb4sPzaNbMiIEGa6LRNdz6PNCt204BldtjgTCAfeKyCykutdLHR3jmkPUh_6YiNx5SFxvODLxxk',
    'isg': 'BJGRwB24kIQc0v1UpCxfEi5joJ0r_gVwC9WtqHMn3NgTGrFsukyJQYw4uO78Ep2o',
    'JSESSIONID': '761647FF418D6DC00C23697E072AC1F9',
    'intl_common_forever': 'Icol511nGM0lol8HdeRhnxyXQSyTvFMITxJz3YncsnmkYkQ6DpnWMQ==',
    'xman_t': 'uEDJtZBRVbGEvp6aBb7HfUM2x2jzNcu/5S2ykuqed70fhzyWftKVvRQX4KYPfEWiVoI+0/HCtbcR6kW3cotzYPHaJRgV4HxVU+WctnGnHDkkqkHtg/rWocYv/9D98mfzqGMtUwbeNghDkstj2YwgmuKooEYvdL3855YL7bWslI5U+Kuq/KUP1K+vaUjxQtFsaT9B9oJxdKeHCGuD1zDLTkmhzJWQqbYxEiLX/KyneX2dOf6II99fCix6Km5hjHy9lWjSPevA6Xgsd69zSunmc0t4i3lrKIZ+fcw8IClffBJnQYrdAAfPKsVdPvhK+AbEO8DYgLRcJCVwxV78b4vAcxRcZeXhkvIBl1Ykw0dn5q5IJ3Kk/52PArirhWNxY9HAnQk9BdZzEb8dXt52xGKMzNd0GE0slUgPahKoCCufhw8d5ZFCeTZhC0tYhXl3EvL3N3fG02+YY5jjzKCmFCqPA+8wimscdNcLtGfpwRbAQ+a5wHcIGLaOMcT3T28XYIvnHDAbHXg9bcpbXH3zXCrLPfr6yzcqSeugjHSJZl5EJhp4tBfFPAuwWZ7IYaHauUHyF21mw+GOzEt/Qv/0D0x563IiILxtg6lDeNJHoWR8jqJBhznVE0MW0a0WwlPInBzumH07ha2+PNsOLrzJ0xJ8VFlmVT8uEkgGjYxM0oKtReYqdC9ldu4G2N3afn1scjmv613P2InSMzuOaCmferTBFU4Ypc+iz+fqX1mCQhE8sh13PwmsGKU8ysMaP1DxtkfzXeDMJ9oTEmw=',
}

headers = {
    'authority': 'www.aliexpress.us',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-ch-ua': '\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
}

params = {
}

response = crawles.get(url, headers=headers, params=params, cookies=cookies)
print(response.text)
TradeCount = re.findall('"formatTradeCount":"(\d+)","tradeCountUnit"', response.text)
print(TradeCount)

