# coding = utf-8
import crawles
import re
import json
import threading
import csv


# 子类目，获取第一页数据
def get_items_1(url, id):
    cookies = {
        'ali_apache_id': '33.8.71.47.1692419810427.274286.4',
        'cna': 'A0NfHbGscV4CAXWTa0ou3K3W',
        '_gcl_aw': 'GCL.1692419935.Cj0KCQjwrfymBhCTARIsADXTabmJf6lkHAgwil2oZf21b_0d1T9QthZ21BekTB55ouO4QLy-64WXopwaAoqbEALw_wcB',
        '_gcl_au': '1.1.926050112.1692419935',
        '_gac_UA-17640202-1': '1.1692419935.Cj0KCQjwrfymBhCTARIsADXTabmJf6lkHAgwil2oZf21b_0d1T9QthZ21BekTB55ouO4QLy-64WXopwaAoqbEALw_wcB',
        '_ym_uid': '1692419936345357159',
        '_ym_d': '1692419936',
        '_hvn_login': '13',
        'x_router_us_f': 'x_alimid=4465986603',
        'aep_common_f': 'ioayHSkvnyaEOULaL/zclkS0aFNPf6RTgi7enhsfna3QWW7fqWPj6w==',
        'af_ss_a': '1',
        'af_ss_b': '1',
        'traffic_se_co': '%7B%7D',
        'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%093256805211698701%092255800466772284',
        'intl_locale': 'en_US',
        'acs_usuc_t': 'x_csrf=ip4wakyxj7r_&acs_rt=0550860dcba6466586d4f7041a8bd5dd',
        'aeu_cid': '53ffb8671830427891832fbd3634ad85-1696743658922-04675-UneMJZVf',
        'xlly_s': '1',
        '_gid': 'GA1.2.977611849.1696743722',
        '_ym_isad': '1',
        'ali_apache_track': 'mt=1|ms=|mid=us2865472608lydae',
        'ali_apache_tracktmp': 'W_signed=Y',
        'havana_tgc': 'NTGC_4f5c750d5fb52f41978bc4954d3b4006',
        'xman_us_t': 'x_lid=us2865472608lydae&sign=y&rmb_pp=zhuowangqian0522@gmail.com&x_user=VDk/0qKNGq1XVZR8fHSaKjiMqDB6SDq7sGrZphxSUIk=&ctoken=xi2bniumld26&l_source=aliexpress',
        'bx_s_t': 'DBXyLXA6CYbnKSto0SDAl6joxHWByMePj8Z5Ba5QB7pGGHLsSTeg8gQH5/OjnLrmbBhWw+XnAPpmr0tlwO1RNHxlKGxtpnlREncPp1LxDQceYHZP3FW0Hc7rbcKUbgxL',
        'sgcookie': 'E100lpmFmcPljukT9gqxSCxD7xXwQg5dV8XF4HcmsEohvkERpqvhYLD8Qb8hxR3f4tG5c0fTRNQie1Y+dE+FSt4h5QWeFkDrwM9hADSCz9ev21k=',
        'xman_f': '5fAYnRp2rbvWeEzmaUfFp0ncXyj99iaG4oyxLH4wE9QfBrXu10MNzDbEZ/oqTdEExvHZCD9zOgeuwjQn/3q/bs88aq2/uN4aYPtuCqrhc5Tl1RzpX61T/YbtuwUFpgP9dW1RhmoNoK6XUzDwccXJwoTd4ZAgnAnfIwm9klb2HWnai5J0f+PjQ1Szn6iQPhPzmNrNb53MZxqp9/xALpM2lX6f5AtX3USFi2Q1/IMeh3GmdVdECg59b8KZm59zbT3DRo5jTvoD5jA6ZfqZMUk5lYR9CNrwEU6QWKunoncSWg4quI29uRs20L8ukFdv2Ty3UQIHvG0bfFEd6XcRAE4yrvBaaHpWoPzoYKuo9px8umj9zs8vpPhpvvPsvtuiG1BFV/9tdBgY8bfRPNOpxb28zgvJ6TlZVhRu6mwyuTF/qs6t3xk9RxlRGpo7+MVPDVvp',
        'aep_usuc_f': 'site=usa&province=922873780000000000&city=922873786976000000&c_tp=USD&x_alimid=4465986603&isb=y&region=US&b_locale=en_US',
        '_m_h5_tk': '2899e242e1d2f458604fc76900bde378_1696751328447',
        '_m_h5_tk_enc': '6de490caf079dc80a1bf955ed040412e',
        '_ym_visorc': 'b',
        '_ga': 'GA1.1.2000821855.1692419935',
        'cto_bundle': 'zZi0dV9QSUhGTFM0RkN3TTk4clRZMUhTeUxFT0JYZjgwTG9xaG03amRkdFZ2MExRY2hZWTBPRTMxWGZYVCUyQlRIQUpiaGtJaldqTzV5aEFuOEU3UFpZQVhDODRDQWlWZFljcDVybzZiNlRoS3RHVFM2RExaczVaSnR3WGZFS2dRSGpSZ1FJMWZldGIxUWpWcFJEUFVMJTJCNlIlMkZPSGtvQU1BQ2habjZ1T2t5N0JpeW9mUlElM0Q',
        'xman_us_f': 'zero_order=y&x_locale=en_US&x_l=0&x_user=US|wangqian|Zhuo|ifm|4465986603&x_lid=us2865472608lydae&x_c_chg=0&x_as_i=%7B%22aeuCID%22%3A%2253ffb8671830427891832fbd3634ad85-1696743658922-04675-UneMJZVf%22%2C%22affiliateKey%22%3A%22UneMJZVf%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cv%22%3A%222%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1696743658922%7D&acs_rt=6837107a988a41f2aeefd19712beff8a',
        'JSESSIONID': 'C7AB5979749FE5B71EB118B07E186A5F',
        'tfstk': 'diOyo1cK_bhrg0nfFT5Fg9Rn5tfRN1n_-BsC-eYhPgjuN7ZH3HtDPLNCO9Ve-eBHN_TW0M-BSLt5N9GH0w7hxwXlribcRiQCVU1QT9YhcHNBPHaJHhTgNQMROW5R96msffG1yUCdt9AR5Atle-flyWGs1ULJng9FefgR3rN5jKbzNyqGFcYCmQdwbZI-6lj_tWAo9TSZFM7AyI7PUGX0uWWNqkQcAwOpUk2FEZQVfqu2W_Xcp',
        'l': 'fBMNRSJRN9SPQ8UoBO5alurza779fBAfGsPzaNbMiIEGC6vdwc9tPixQV7vSkKKRR8XPgUYB4daEEWvt1eDT-ykfnSI97VaS2_x2Ie8C582bY',
        'isg': 'BCoqiJwHO8eIRrZpow3F88v6e5DMm671BLgmtbTltHzH586hnCqIBA5VdxN7FyaN',
        'intl_common_forever': 'KqR0vVQFlaC5+VHOAfcLD90osvmlcAxwd7FD2MYMKgyOtOt5QK9uPg==',
        'xman_t': 'efs42sB3dJ5I+omH5TA5ju1bjneMMUeK6oEzFgL1LbbZ0p6O18PCKyGmDcKtV+DIx+ONxstogTibNp6n08paC/na5/+StNFKNnJvT4jQju57/pLj83lgFdGMWyPJy9bCjT30KYwcy8/ee365RZsSpVjyebw4K/mUtiLa0H64I/GR7pttCfGW8mwfnQqdOapkJsn/RqeBJQ55w9k2HSTup02VlBmKM9sx3gOV+KL/pDzsWZgkhWhAi09gLZyAVPUDcRdCP8S7CK8ji4NQ5YchCLw0MxasSed/EdQ5ETE1fR6EhL6sbIQFAHJGSH/K82JPUKxwWb4MWDzRmKbqd8ehF262o5naFzCcCLqt4bP5XuB5J+1FWW6oG9r7yuHwf53V6q6/t8SwHH7bMElrOYfxjrz7mmkESYhYFTY3fyos5l7Db62tXPmHrJim1vcBLWhLubIJoyWhGdFvuJ9DJshlWZghR52uiNAZvd4/KbWLtdQkJNwEnbLMcTnMRgJPhtzfg94J3jpdYFubq/fqh0vvWsX5RzKfrjMMDC5sUKP56jcEfJ87ctbp/szocd3iztAc6UclsFNnV3OPkcJQoTgWMp3MFCblD/9iNiAnZsc5FP9Ud0CVuupmX71LdZZUy5U/qG/vVhVFhMGL9x4pZw6RDfoe/9NVTXZ8/Dkn2EteaHGL/E5Y+8cJW7xycjqfechb2SYiMH/xk9HktStxRGUq4IlhgzBn+77y22250HVanceX2/xbVYjfyy3p32HMzXggGZV2qH8WAhA=',
        '_ga_VED1YSGNC7': 'GS1.1.1696748896.9.1.1696749770.51.0.0',
    }

    headers = {
        'authority': 'www.aliexpress.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'dnt': '1',
        'referer': 'https://www.aliexpress.com/category/100003109/women-clothing.html?category_redirect=1&spm=a2g0o.home.101.1.468a2145h5JWeD',
        'sec-ch-ua': '\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    params = {
        'CatId': id,
        'g': 'y',
        'isCategoryBrowse': 'true',
        'isrefine': 'y',
        'trafficChannel': 'ppc',
    }

    response = crawles.get(url=url, headers=headers, params=params, cookies=cookies).text
    contents = re.findall('"itemList":(.*?),"_cost"', response)
    return contents


# 获取主类目id(abandon)
def request_get2():
    import crawles
    url = 'https://www.aliexpress.us/api/data_homepage.do'
    cookies = {
        'aep_common_f': 'S/MVm6T6yJbDgpwuZLp0+mepUxJIsAcSCB6JXoNYXlM/BGzIEblZbw==',
        '_ga_save': 'yes',
        'cna': 'A0NfHbGscV4CAXWTa0ou3K3W',
        '_gcl_au': '1.1.313344858.1692420089',
        '_ym_uid': '1692420095424565094',
        '_ym_d': '1692420095',
        'x_router_us_f': 'x_alimid=4465986603',
        'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%093256803817028291',
        'intl_locale': 'en_US',
        'acs_usuc_t': 'x_csrf=dqox7rngq674&acs_rt=8d0910d341124476ba8f0dc68be43635',
        'xlly_s': '1',
        '_gid': 'GA1.2.26933144.1696743660',
        '_gac_UA-17640202-1': '1.1696743660.CjwKCAjwg4SpBhAKEiwAdyLwvMdAaECMCsHES3QOKMKoNo22ssNIwZh47mSeb7zTCPZmvabeza3GLxoCHugQAvD_BwE',
        '_gcl_aw': 'GCL.1696743660.CjwKCAjwg4SpBhAKEiwAdyLwvMdAaECMCsHES3QOKMKoNo22ssNIwZh47mSeb7zTCPZmvabeza3GLxoCHugQAvD_BwE',
        '_ym_isad': '1',
        'xman_us_t': 'x_lid=us2865472608lydae&sign=y&rmb_pp=zhuowangqian0522@gmail.com&x_user=VDk/0qKNGq1XVZR8fHSaKo+ig5n1ewU6iGiRAOR4s6c=&ctoken=i6mzn__ya93w&l_source=aliexpress',
        'bx_s_t': 'DBXyLXA6CYbnKSto0SDAl6joxHWByMePj8Z5Ba5QB7pGGHLsSTeg8gQH5/OjnLrmbBhWw+XnAPpmr0tlwO1RNHxlKGxtpnlREncPp1LxDQceYHZP3FW0Hc7rbcKUbgxL',
        'sgcookie': 'E100qjzzRmgYY1Thrkb/V7YOw/l1SlhU/OyIS36U0FVXPtxCjUzUtaM7gS6YKaKFXqDlxEa+ZGNVpKciBY15BxysUpuwDPxJn/4ZR5woFgohkY0=',
        'xman_f': 'ALEcBxzxOBbggoJtqzCe95ManQNEhTd409SezFjg37h5JGx8Rnzb9A7k0CRPFQ+lEH5ByEbZXszH1SSns68iTLUcYW4wxMm54oDSWpmubLX+PA+7Z4k08C/MRF+u5jNL583DvaycAMbi9oaNtD1db51n2XdW0RmxZPOFE6S0cb2rkzRg56f6HIBunyT4s0XJA7DCdrbhZYd0V6ztE+8PvRY96qeUgf0BAGJzCmZJ9Wg1A3hAT0OFkkabIKSMv63D7hFmLi570rtx8QgeRZihhd13xUn2t1kub8RIR74zfVvue/zfldd969IAEI6+I51fOLik2N8CfVzKLGv+sXKMbQgmAjTXorweVo2W7MlRnWT9zx5RCLzamaXP65csSa2xIC36mXGWiyXxqCO5L1hT+m+wObeIAs3DU4e9qQErdbH/jgxeLonImVwC383r397f',
        'aep_usuc_f': 'site=usa&province=922873780000000000&city=922873786976000000&c_tp=USD&x_alimid=4465986603&isb=y&region=US&b_locale=en_US',
        'AKA_A2': 'A',
        'xman_us_f': 'zero_order=y&x_locale=en_US&x_l=0&x_user=US|wangqian|Zhuo|ifm|4465986603&x_lid=us2865472608lydae&x_c_chg=0&x_c_synced=0&x_as_i=%7B%22aeuCID%22%3A%22adb805cc37ca48488675dba82c1e7d03-1695792061558-07676-UneMJZVf%22%2C%22af%22%3A%22178094261%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cookieCacheEffectTime%22%3A1695897468380%2C%22isCookieCache%22%3A%22Y%22%2C%22ms%22%3A%220%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1695792061558%7D&acs_rt=6837107a988a41f2aeefd19712beff8a',
        '_m_h5_tk': '57a613967abfd21c45b0d6b029139a44_1696754064151',
        '_m_h5_tk_enc': '1c48bf0b4c66def83e62fcdf916de691',
        '_ym_visorc': 'b',
        'JSESSIONID': '5002970B56F73BD9B723394C99C5F057',
        '_ga_VED1YSGNC7': 'GS1.1.1696752177.6.1.1696752763.41.0.0',
        '_ga': 'GA1.1.2000821855.1692419935',
        'cto_bundle': 'JrcrcF8zT3ROck04NkZkUjNiWXZRaUFkQUpSYXlTR3JNUlduNGFTZFc0NzRMdmNNWnJnTkNmQk5pbWh4QmlYdUw2JTJGQ3hwVEJNJTJCV1ZnYlB5SzJvNVB4clRsanRkdFpBYSUyQmZGUjlxak1zS1lFNzIxVDlTcnNaUHM2bVgzVEVXcGgweWlxZVAxUnRwM2NVa01CdU9NMmZJJTJGUW9VMkxhV0U1ZUxiNExDNDNjODBPWG9SUSUzRA',
        'intl_common_forever': 'yiuWyQVGihWSH4D3PCd554xcSXTrSl98QKF54rUYPojANhEQLI+LVg==',
        'xman_t': 'JO+RKnl3QSsThqPRPG8yJ5X9HKhFKotM+WBEQiiSpHnDZDSkDWmTHqlAyLJk55Sc5LtQyVeWFqyJcBiXYNTD9WEHiBnisBEQ0g3sq6hE94RryF88PsTRDrTtsSckLNcQsRHVvF77F0usf6PGuEQNVjHWdF91o7lNx3/je74d8GCVBPBPlhWKfftoqQKUO+N8tb5RXWaLn+rxH92qdS8eTaSgV6RvJhbvSHe9pu9Oe6AjOO5uI+ZBDeYQqPF7dHJK1Bs1KH8PBrEybl8NjXTXdbw8/Q4X571OKEk1euqkTqxF82Lxze3Eqf4WQDZPnDl/h2MO6D+lXvfWXhHouav/d8YEXRaHaxLFu4Hswge/3pzlyovWe10ch+oyPjoFgoijWki4xKHRRM2EDAtClhQjUm398mzZ5U7akdrgNJZhnsE/0J9dWuBAjgqZ0bnv17yeBQv9bjtb3nM+0isoFsmX2uepywxnOfUk+u/dPQ2H+/JPzE6ZKwnv9o4/aLulibVZ4gkRcqaUSVG/zA0lEf2xPRe9ljZwhFGKte3rFn9j2t7mrAYEsL7sXlx3/kP2MCxaP+XRtmwvIA3g8gvgHup/0Pmom6WxqWApqvEt2ReV9imvIJIan+DaNrQSNZYvFIogYoC86aKANS0eHNUXR7k3R+hVTyGQDoaDvO/IPysZbiBspAVElZdFq2vsAiziSmSu1wflJ2UniZjptyz6zZ81IiVJorH8CFoze/dd7+B/sJoYYpmpvji5+4IIqrKpr2853GUaf17q/dM=',
        'isg': 'BHl5EBCYOEqj4eUcTKTHykZ7iOVThm04892V4Juu6KAfIpm049bcCPYzpCbUmgVw',
        'l': 'fBTfACbeN9STyvAGBOfwFurza77O_IRAguPzaNbMi9fP9h1e5n05W1n4a78wCnGVF6uDR3J_8YVHBeYBq_C-nxvO7zqvhCMmn_vWSGf..',
        'tfstk': 'dIKXh5GwPSVbgAYA7RMyNdwyXVj6cIiU5R69KdE4BiIY65pdaxjwux29BdOQ0oJO31d5m384bslcfddFfXlEYDJDnMjtTXk-SKvDYm8CvDoenKYRgF_mYxb5CoI6rx4nRzpjNor0Y9x6lSeFnTx5ha3yH_U5_36f46pvclBNzk5I_vz_Fwq1F6kSFP4ieqBf0',
    }

    headers = {
        'authority': 'www.aliexpress.us',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'dnt': '1',
        'referer': 'https://www.aliexpress.us/?gatewayAdapt=glo2usa',
        'sec-ch-ua': '\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '\"Windows\"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    params = {
        'featuresWhitelist': '1',
        'gatewayAdapt': 'glo2usa',
    }

    response = crawles.get(url, headers=headers, params=params, cookies=cookies)
    # print(response.text)
    text = re.findall('/www.aliexpress.com/category/(.*?).html', response.text)
    return text


# 获取子类目商品id（abandon）
def request_get3():
    id = request_get2()
    dict2 = {}
    for index, i in enumerate(id):
        url = f'https://www.aliexpress.com/category/{i}.html'
        cookies = {
            'ali_apache_id': '33.8.71.47.1692419810427.274286.4',
            'cna': 'A0NfHbGscV4CAXWTa0ou3K3W',
            '_gcl_aw': 'GCL.1692419935.Cj0KCQjwrfymBhCTARIsADXTabmJf6lkHAgwil2oZf21b_0d1T9QthZ21BekTB55ouO4QLy-64WXopwaAoqbEALw_wcB',
            '_gcl_au': '1.1.926050112.1692419935',
            '_gac_UA-17640202-1': '1.1692419935.Cj0KCQjwrfymBhCTARIsADXTabmJf6lkHAgwil2oZf21b_0d1T9QthZ21BekTB55ouO4QLy-64WXopwaAoqbEALw_wcB',
            '_ym_uid': '1692419936345357159',
            '_ym_d': '1692419936',
            '_hvn_login': '13',
            'x_router_us_f': 'x_alimid=4465986603',
            'aep_common_f': 'ioayHSkvnyaEOULaL/zclkS0aFNPf6RTgi7enhsfna3QWW7fqWPj6w==',
            'af_ss_a': '1',
            'af_ss_b': '1',
            'traffic_se_co': '%7B%7D',
            'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%093256805211698701%092255800466772284',
            'intl_locale': 'en_US',
            'acs_usuc_t': 'x_csrf=ip4wakyxj7r_&acs_rt=0550860dcba6466586d4f7041a8bd5dd',
            'aeu_cid': '53ffb8671830427891832fbd3634ad85-1696743658922-04675-UneMJZVf',
            '_m_h5_tk': '80990490b3ae828388182dfa4679c5b0_1696745698062',
            '_m_h5_tk_enc': 'f460866eab978f4f9590374d7fd7ff6b',
            'xlly_s': '1',
            '_gid': 'GA1.2.977611849.1696743722',
            '_ym_isad': '1',
            '_ym_visorc': 'b',
            'ali_apache_track': 'mt=1|ms=|mid=us2865472608lydae',
            'ali_apache_tracktmp': 'W_signed=Y',
            'havana_tgc': 'NTGC_4f5c750d5fb52f41978bc4954d3b4006',
            'xman_us_t': 'x_lid=us2865472608lydae&sign=y&rmb_pp=zhuowangqian0522@gmail.com&x_user=VDk/0qKNGq1XVZR8fHSaKjiMqDB6SDq7sGrZphxSUIk=&ctoken=xi2bniumld26&l_source=aliexpress',
            'bx_s_t': 'DBXyLXA6CYbnKSto0SDAl6joxHWByMePj8Z5Ba5QB7pGGHLsSTeg8gQH5/OjnLrmbBhWw+XnAPpmr0tlwO1RNHxlKGxtpnlREncPp1LxDQceYHZP3FW0Hc7rbcKUbgxL',
            'sgcookie': 'E100lpmFmcPljukT9gqxSCxD7xXwQg5dV8XF4HcmsEohvkERpqvhYLD8Qb8hxR3f4tG5c0fTRNQie1Y+dE+FSt4h5QWeFkDrwM9hADSCz9ev21k=',
            'xman_f': '5fAYnRp2rbvWeEzmaUfFp0ncXyj99iaG4oyxLH4wE9QfBrXu10MNzDbEZ/oqTdEExvHZCD9zOgeuwjQn/3q/bs88aq2/uN4aYPtuCqrhc5Tl1RzpX61T/YbtuwUFpgP9dW1RhmoNoK6XUzDwccXJwoTd4ZAgnAnfIwm9klb2HWnai5J0f+PjQ1Szn6iQPhPzmNrNb53MZxqp9/xALpM2lX6f5AtX3USFi2Q1/IMeh3GmdVdECg59b8KZm59zbT3DRo5jTvoD5jA6ZfqZMUk5lYR9CNrwEU6QWKunoncSWg4quI29uRs20L8ukFdv2Ty3UQIHvG0bfFEd6XcRAE4yrvBaaHpWoPzoYKuo9px8umj9zs8vpPhpvvPsvtuiG1BFV/9tdBgY8bfRPNOpxb28zgvJ6TlZVhRu6mwyuTF/qs6t3xk9RxlRGpo7+MVPDVvp',
            'aep_usuc_f': 'site=usa&province=922873780000000000&city=922873786976000000&c_tp=USD&x_alimid=4465986603&isb=y&region=US&b_locale=en_US',
            'JSESSIONID': '6C253D14E2CA772D0974E0B7ED644B8A',
            '_ga_VED1YSGNC7': 'GS1.1.1696743723.8.1.1696744760.60.0.0',
            '_ga': 'GA1.1.2000821855.1692419935',
            'cto_bundle': 'DoWPgl9QSUhGTFM0RkN3TTk4clRZMUhTeUxGdkEwMjM4T1hVWSUyRmgxbCUyQlFFSUIxMkZnV2tyNTZVYTFEUmZjeHElMkZCcVhESEE3Yk5mYzYlMkZuZFFoOGJvU0JtdE5BeGlqYnlnVnQxbHJqTEwxelNWNTdic3N3RjRpRWdOWW9VYVJaUVVsYk1KWCUyQk5qemVUNUhiY3czbmV2R2cyQ2xOeXB6aGJXRVhjYWVzU3hqdm4yZlBnJTNE',
            'tfstk': 'dKzko4VBRuo5ND9Sxg35zqjfSXjxNLgIgJLKp2HF0xkXeLL8T2f3eRvKpDCSLvk0dYn-zTgnTReseXK-zmPqOXhy4Yky0-23hyd-ebQnTWkYpeF8pQZbB588yggp-4gI8OBOWNh7N2gEK-bOWlS2vWWOBNQTHi0goOERx655UqXhmyqMoXiPh5AU0zBF94DaaYP8wrlDBAPr3e8EEbXasn-Z5YTIg6U2AHirGjDtqsK1l',
            'l': 'fBMNRSJRN9SPQ_G2XOfZPurza779jIRAguPzaNbMi9fPObfH5vtNW1n42sTMCnGVFsIeR3J_8YVHBeYBq1jrukhuGQ0oOXkmn_vWSGf..',
            'isg': 'BAUFdo9kzKY1Kuk4METy8kjjFEE_wrlUp9GZhAdqxTxLniUQzxMtJMU0rMJo3tEM',
            'xman_us_f': 'zero_order=y&x_locale=en_US&x_l=0&x_user=US|wangqian|Zhuo|ifm|4465986603&x_lid=us2865472608lydae&x_c_chg=0&x_as_i=%7B%22aeuCID%22%3A%2253ffb8671830427891832fbd3634ad85-1696743658922-04675-UneMJZVf%22%2C%22affiliateKey%22%3A%22UneMJZVf%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cv%22%3A%222%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1696743658922%7D&acs_rt=6837107a988a41f2aeefd19712beff8a',
            'intl_common_forever': '/eJD2VqQHyDnLINAs2gFJysIZvd/lJ8CB8DWXh80oJ3lH0p4ksbR5w==',
            'xman_t': 'Eujlx267uD5cZgxrbXP97Jf45oyOwp+6BOuKzeQehM5hLWIWriGguk70UaO3hTfuG/DFRJ3S9DsPF4tcetK4W1ryJa9NQwHI4xmGuNqUk3o0esrAsky08h3fmdeH1RRRPy5QhZ+t0Smf/EuocCCfpqJDna2O7hk2maJay7N7vKjni+6AbZKO+trLbw5UegfQrwWYSN0nxSgaiaNmopUTzZrpf82C9FcBd1q2zL/u58BtmZRvEFzzJI/BaxldXDnpw4AO9y/Bm1UwNmcV0N2JU0lCps3x6XG/B0/3BDi02fArMz4Mb5yXeBz/ZcX7KV8zoVigP8aC7SPxxiTYjiFruyHdY3j8/R1D/Q0oe+wovOgL3jvMU/iN1QSN2kGILIe9rs1DgpzlCS0jZnGLHG//yDIntVY650k3OiIto5pp1heFX9L7C94tibQ6nhxC1ZkNesrin3COHxe/VbT2VqM6x8eyhVmiHmCF4izeLE+ap9xZpmfUc+XD1p4wof2U1xp+QqEYtBw5i67B8cU373O8rNfswrxBnPCyEyzORcVlAAelIk7omIel8skRWS6blo+y7BUqA0u1OjabG1xSXe2v9s6PBjzIV6R016vsXwI9zeUfVqv5Iknusa04XRyV12/d1Zq5a2G1aFr+DXEoMeyv7tfZQOUzoCONybtlhs8G4m/hKmY24ISpIfrOyaXyc83aS4ZLGM9dchrqzLy5eSjR9sulHkYL2Um9xXWGu1BGYt4C99rOSIZSG2nwqzVFWv/0mgNAB0JgADE=',
        }
        headers = {
            'authority': 'www.aliexpress.com',
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
            'category_redirect': '1',
            'spm': 'a2g0o.home.101.1.468a2145h5JWeD',
        }
        response = crawles.get(url, headers=headers, params=params, cookies=cookies)
        text = re.findall('"title":"Categories","content":\[(.*?)],"rapidTiling"', response.text)
        dict = json.loads(text[0])
        categoryId = dict['categoryId']
        categoryEnName = dict["categoryEnName"]
        childCategories = dict["childCategories"]
        childCategories_dict = {}
        for childCategory in childCategories:
            childCategories_id = childCategory['categoryId']
            childCategories_Name = childCategory['categoryEnName']
            dict1 = {childCategories_id: childCategories_Name}
            childCategories_dict.update(dict1)
        dict0 = {categoryEnName: childCategories_dict}
        dict2.update(dict0)
    return dict2


def get_data_model():
    data = {
        'item_url': None,
        'sale_num': None,
        'imageurl': None,
        'productId': None,
        'storeUrl': None,
        'aliMemberId': None,
        'storeName': None,
        'storeId': None,
        'displayTitle': None,
        'seoTitle': None,
        'clickurl': None,
        'lunchTime': None,
        'builderType': None,
        'taxRate': None,
        'pricesStyle': None,
        'formatted_price2': None,
        'minPriceDiscount': None,
        'cent_price': None,
        'minPrice': None,
        'priceType': None,
        'discount': None,
        'currencyCode': None,
        'productType': None,
        'sellingPoints': None,
    }
    return data


# 获取页面数据
def get_items_all(id, page):
    url = 'https://www.aliexpress.com/fn/search-pc/index'

    cookies = {
        'ali_apache_id': '33.8.71.47.1692419810427.274286.4',
        'cna': 'A0NfHbGscV4CAXWTa0ou3K3W',
        '_gcl_aw': 'GCL.1692419935.Cj0KCQjwrfymBhCTARIsADXTabmJf6lkHAgwil2oZf21b_0d1T9QthZ21BekTB55ouO4QLy-64WXopwaAoqbEALw_wcB',
        '_gcl_au': '1.1.926050112.1692419935',
        '_gac_UA-17640202-1': '1.1692419935.Cj0KCQjwrfymBhCTARIsADXTabmJf6lkHAgwil2oZf21b_0d1T9QthZ21BekTB55ouO4QLy-64WXopwaAoqbEALw_wcB',
        '_ym_uid': '1692419936345357159',
        '_ym_d': '1692419936',
        '_hvn_login': '13',
        'x_router_us_f': 'x_alimid=4465986603',
        'aep_common_f': 'ioayHSkvnyaEOULaL/zclkS0aFNPf6RTgi7enhsfna3QWW7fqWPj6w==',
        'af_ss_a': '1',
        'af_ss_b': '1',
        'traffic_se_co': '%7B%7D',
        'aep_history': 'keywords%5E%0Akeywords%09%0A%0Aproduct_selloffer%5E%0Aproduct_selloffer%093256805211698701%092255800466772284',
        'intl_locale': 'en_US',
        'acs_usuc_t': 'x_csrf=ip4wakyxj7r_&acs_rt=0550860dcba6466586d4f7041a8bd5dd',
        'aeu_cid': '53ffb8671830427891832fbd3634ad85-1696743658922-04675-UneMJZVf',
        'xlly_s': '1',
        '_gid': 'GA1.2.977611849.1696743722',
        '_ym_isad': '1',
        'ali_apache_track': 'mt=1|ms=|mid=us2865472608lydae',
        'ali_apache_tracktmp': 'W_signed=Y',
        'havana_tgc': 'NTGC_4f5c750d5fb52f41978bc4954d3b4006',
        'xman_us_t': 'x_lid=us2865472608lydae&sign=y&rmb_pp=zhuowangqian0522@gmail.com&x_user=VDk/0qKNGq1XVZR8fHSaKjiMqDB6SDq7sGrZphxSUIk=&ctoken=xi2bniumld26&l_source=aliexpress',
        'bx_s_t': 'DBXyLXA6CYbnKSto0SDAl6joxHWByMePj8Z5Ba5QB7pGGHLsSTeg8gQH5/OjnLrmbBhWw+XnAPpmr0tlwO1RNHxlKGxtpnlREncPp1LxDQceYHZP3FW0Hc7rbcKUbgxL',
        'sgcookie': 'E100lpmFmcPljukT9gqxSCxD7xXwQg5dV8XF4HcmsEohvkERpqvhYLD8Qb8hxR3f4tG5c0fTRNQie1Y+dE+FSt4h5QWeFkDrwM9hADSCz9ev21k=',
        'xman_f': '5fAYnRp2rbvWeEzmaUfFp0ncXyj99iaG4oyxLH4wE9QfBrXu10MNzDbEZ/oqTdEExvHZCD9zOgeuwjQn/3q/bs88aq2/uN4aYPtuCqrhc5Tl1RzpX61T/YbtuwUFpgP9dW1RhmoNoK6XUzDwccXJwoTd4ZAgnAnfIwm9klb2HWnai5J0f+PjQ1Szn6iQPhPzmNrNb53MZxqp9/xALpM2lX6f5AtX3USFi2Q1/IMeh3GmdVdECg59b8KZm59zbT3DRo5jTvoD5jA6ZfqZMUk5lYR9CNrwEU6QWKunoncSWg4quI29uRs20L8ukFdv2Ty3UQIHvG0bfFEd6XcRAE4yrvBaaHpWoPzoYKuo9px8umj9zs8vpPhpvvPsvtuiG1BFV/9tdBgY8bfRPNOpxb28zgvJ6TlZVhRu6mwyuTF/qs6t3xk9RxlRGpo7+MVPDVvp',
        'aep_usuc_f': 'site=usa&province=922873780000000000&city=922873786976000000&c_tp=USD&x_alimid=4465986603&isb=y&region=US&b_locale=en_US',
        '_m_h5_tk': '2899e242e1d2f458604fc76900bde378_1696751328447',
        '_m_h5_tk_enc': '6de490caf079dc80a1bf955ed040412e',
        '_ym_visorc': 'b',
        'JSESSIONID': 'C7AB5979749FE5B71EB118B07E186A5F',
        'intl_common_forever': 'O67P1BbA3q5U95HepCh0alPdpbvIt/R9awHSwCLK+KZJZWhWQL0sFg==',
        'xman_t': 'yk50n6rhlsti+l1oXkBjdBYw12HPMjIDGiCHFlE1t606hvVraPOqKQHsLtjtF5a026yfKotwU9xiJePIHLQL1jElz4iz1hv3r1b34edduUcseOAJ30e93y05G27msd10fmRD1VZm0r0DM+976Oeh6fXanb+IHyCyqe3Ync+ODOHgsareBU1kt1X4/Wp8OXpftB2hppKBP920rMSUtkkJFt2dg6mG1DWc/YCHF/3fcngMdv/sHvMM+gpvNAD+CqqLm6ZGBy1tdY1k/uwmjCzme++pVsY2lo/h+Znw/vp07HiIM7JfeAcu6d8KTcNHOlm3eQ81ujTv+suUE7TS+kkdo3DhtgTl2LBOcqLiIXJbCLml6TNbYcNzcYN1ju53NvvnJcQWRWUXJdjUpy6IEmfyj8itlsromob/CKKHSCvHzEiLe4QSbOktQpIwbFJSJDQgIxG1q6h+MhJvWbB96hPOIgViXPSS55PpZ0ssi68Ytm6p0P7HMIFJz5VjkfsMxe7nt30f6jBlhpL1lWrPzjHshy+hdCB+ZMJ6KRf6bWDx91Kt6DDbzhVwx4pZd9HeHOO8p+Lx4gibV/NgzsVodCCwFvAoiCKjMUsM0iyl+9wvLKeM2LhphNorWJSe4yhewWwmiXLcm2DmErrVNdpG5ycOLQk3Y+DnmNTikC9BqHp5FhXJuycn6QAgm4+RbrhKidZV/hIL86flHbyrbVzXtcQDDQiVlHS8F+FJOvTGdG4JRTnG+2t4cRQHJcAuvosuILcrEVV/XkaoW5A=',
        'xman_us_f': 'x_lid=us2865472608lydae&x_l=0&x_locale=en_US&x_c_chg=0&x_user=US|wangqian|Zhuo|ifm|4465986603&zero_order=y&acs_rt=6837107a988a41f2aeefd19712beff8a&x_as_i=%7B%22aeuCID%22%3A%2253ffb8671830427891832fbd3634ad85-1696743658922-04675-UneMJZVf%22%2C%22affiliateKey%22%3A%22UneMJZVf%22%2C%22channel%22%3A%22PREMINUM%22%2C%22cv%22%3A%222%22%2C%22isCookieCache%22%3A%22N%22%2C%22ms%22%3A%221%22%2C%22pid%22%3A%22178094261%22%2C%22tagtime%22%3A1696743658922%7D',
        '_ga': 'GA1.1.2000821855.1692419935',
        'cto_bundle': 'FcFa119QSUhGTFM0RkN3TTk4clRZMUhTeUxDSDdXZmREbVJqNUtoa2dqRkh5ajI0RjAyT0Z6bHYwYW5XY2prTThwejhGRTBLOXJnVGpVWFhBMkpwbkYlMkZYaUFDOXZ6Y2FxQjJid3kzUGs0cyUyRll1aWVPajIwV1ZXS1h0ZmF5RXVYU3lXbkhhNm04SmZ4bTBSWU90TU1HZSUyRmF1JTJGVmpFdU1iR0YlMkJzU2VvQzkwZmFPTXNVJTNE',
        '_ga_VED1YSGNC7': 'GS1.1.1696748896.9.1.1696751049.60.0.0',
        'tfstk': 'dZHeosvJ3ppeQeL_OWyzQ7llf02LU-LfqYa7q0muAy4hd9_o_4giAX67F7Xrq0FodJiI7zuSmXgQd79o7ururuV3xPqgVPE7RDw5U7mu546SA4sK6qicdvOLFTyLe8YXlK9bvDe8EA42QFw49123vT9XhDnKsyGz9KtL_A6hjKGFasxY9Em7SvHqkt0ep30lETDHe5a2TzqTxA53iznnLCXaZaEgPuM-TafztlEalh-ZDJVgw',
        'l': 'fBMNRSJRN9SPQbk6BO5alurza779CBRffsPzaNbMiIEGa6QdtgGmdNCt0yVySdtjgT5qlF-yCykutdEv87438x60MGLZ5ziRZEJWWe__E-ZF.',
        'isg': 'BKamD7lS_xOx8Kp1h-EBpycu9xwoh-pBGGwaiZBJc0kLE0Et_xalUK2law-fu-JZ',
    }

    headers = {
        'authority': 'www.aliexpress.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'bx-v': '2.5.3',
        'content-type': 'application/json;charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.aliexpress.com',
        'referer': 'https://www.aliexpress.com/category/200215341/rompers.html?CatId=200215341&g=y&isCategoryBrowse=true&isrefine=y&trafficChannel=ppc&page=2',
        'sec-ch-ua': r'\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': r'\"Windows\"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    }

    params = {
        "pageVersion": "662440442fbbefbab6460b18b9c3631b",
        "target": "root",
        "data": {
            "CatId": id,
            "g": "y",
            "isCategoryBrowse": 'true',
            "isrefine": "y",
            "page": page,
            "trafficChannel": "ppc",
            "origin": "y"
        },
        "eventName": "onChange",
        "dependency": []
    }
    count = 0
    while count <= 5:
        try:
            response = crawles.post(url, headers=headers, json=params, cookies=cookies, timeout=5).text
            response1 = re.findall('"itemList":\{"content":(.*?),"legalJeopardyInfo"', response)
            if response1 == []:
                response1 = re.findall('"itemList":\{"content":(.*?),"__context"', response)
            res = '{"content":' + response1[0]
            res1 = json.loads(res)
            contents = res1['content']
            return contents
        except:
            count += 1
            continue


# 数据清洗
def clean_data(content):
    data = get_data_model()
    imageurl = content['image']['imgUrl']
    productId = content['productId']
    storeUrl = content['store']['storeUrl'].replace('//', '')
    aliMemberId = content['store']['aliMemberId']
    storeName = content['store']['storeName']
    storeId = content['store']['storeId']
    try:
        displayTitle = content['title']['displayTitle']
    except:
        displayTitle = 'None'
    try:
        seoTitle = content['title']['seoTitle']
    except:
        seoTitle = 'None'

    try:
        clickurl = content['p4p']['clickUrl']
    except:
        clickurl = 'None'
    try:
        lunchTime = content['lunchTime']
    except:
        lunchTime = 'None'
    try:
        builderType = content['prices']['builderType']
    except:
        builderType = 'None'
    try:
        taxRate = content['prices']['taxRate']
    except:
        taxRate = 'None'

    try:
        pricesStyle = content['prices']['pricesStyle']
    except:
        pricesStyle = 'None'
    try:
        formatted_price = content['prices']['salePrice']['formattedPrice']
    except:
        formatted_price = 'None'

    try:
        minPriceDiscount = content['prices']['salePrice']['minPriceDiscount']
    except:
        minPriceDiscount = 'None'
    try:
        cent_price = content['prices']['salePrice']['cent']
    except:
        cent_price = 'None'

    try:
        minPrice = content['prices']['salePrice']['minPrice']
    except:
        minPrice = 'None'

    try:
        priceType = content['prices']['salePrice']['priceType']
    except:
        priceType = 'None'

    try:
        discount = content['prices']['salePrice']['discount']
    except:
        discount = 'None'
    try:
        currencyCode = content['prices']['salePrice']['currencyCode']
    except:
        currencyCode = 'None'
    try:
        productType = content['productType']
    except:
        productType = 'None'
    try:
        sellingPoints = content['sellingPoints']
    except:
        sellingPoints = 'None'

    data['imageurl'] = imageurl
    data['productId'] = productId
    data['storeUrl'] = storeUrl
    data['aliMemberId'] = aliMemberId
    data['storeName'] = storeName
    data['displayTitle'] = displayTitle
    data['storeId'] = storeId
    data['seoTitle'] = seoTitle
    data['clickurl'] = clickurl
    data['lunchTime'] = lunchTime
    data['builderType'] = builderType
    data['taxRate'] = taxRate
    data['pricesStyle'] = pricesStyle
    data['formatted_price'] = formatted_price
    data['minPriceDiscount'] = minPriceDiscount
    data['cent_price'] = cent_price
    data['minPrice'] = minPrice
    data['priceType'] = priceType
    data['discount'] = discount
    data['currencyCode'] = currencyCode
    data['productType'] = productType
    data['sellingPoints'] = sellingPoints
    data['item_url'] = f'https://www.aliexpress.us/item/{productId}.html'
    # try:
    #     sale_num = get_sale_num(f'https://www.aliexpress.us/item/{productId}.html')
    #     data['sale_num'] = sale_num
    # except:
    #     data['sale_num'] = 'None'
    return data


def get_sale_num(url):
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
    response = crawles.get(url=url, headers=headers, params=params, cookies=cookies, timeout=5)
    TradeCount = re.findall('"formatTradeCount":"(\d+)","tradeCountUnit"', response.text)
    return TradeCount


def save_text(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(data)


def save_to_csv(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['item_url',
                             'imageurl',
                             'productId',
                             'storeUrl',
                             'aliMemberId',
                             'storeName',
                             'storeId',
                             'displayTitle',
                             'seoTitle',
                             'clickurl',
                             'lunchTime',
                             'builderType',
                             'taxRate',
                             'pricesStyle',
                             'formatted_price2',
                             'minPriceDiscount',
                             'cent_price',
                             'minPrice',
                             'priceType',
                             'discount',
                             'currencyCode',
                             'productType',
                             'sellingPoints'])
        for i, values in enumerate(data['item_url']):
            csv_writer.writerow([data['item_url'][i],
                                 data['imageurl'][i],
                                 data['productId'][i],
                                 data['storeUrl'][i],
                                 data['aliMemberId'][i],
                                 data['storeName'][i],
                                 data['storeId'][i],
                                 data['displayTitle'][i],
                                 data['seoTitle'][i],
                                 data['clickurl'][i],
                                 data['lunchTime'][i],
                                 data['builderType'][i],
                                 data['taxRate'][i],
                                 data['pricesStyle'][i],
                                 data['formatted_price2'][i],
                                 data['minPriceDiscount'][i],
                                 data['cent_price'][i],
                                 data['minPrice'][i],
                                 data['priceType'][i],
                                 data['discount'][i],
                                 data['currencyCode'][i],
                                 data['productType'][i],
                                 data['sellingPoints'][i]])

def crawl_thread(child_url, id):
    # try:
    #     contents0 = get_items_1(child_url, id)
    #     data0 = clean_data(contents0)
    #     for add in addData.keys():
    #         addData[add].append(data0[add])
    # except:
    #     print(child_url, id, 'error')

    for page in range(2, 100):
        try:
            print(id, page)
            contents = get_items_all(id, page)

            for content in contents:
                data1 = clean_data(content)
                for add in addData.keys():
                    addData[add].append(data1[add])
        except:
            print(id, page, "error")
            break

# 数据处理
def process_data():
    # 类目以及对应id
    dict = {
        "Women's Clothing": {200215341: 'Rompers', 200215336: 'Bodysuits', 205927403: 'Pants & Capris',
                             205871601: 'Dress',
                             205876401: 'Skirt', 205874801: 'Jeans', 206081401: 'Muslim Fashion', 200118010: 'Bottoms',
                             206083901: 'Plus size clothes', 205895301: 'Swimsuit', 205900902: 'Women Tops',
                             200001648: 'Blouses & Shirts', 200003482: 'Dresses', 200001092: 'Jumpsuits',
                             200000783: 'Sweaters', 200000782: 'Suits & Sets', 200000775: 'Jackets & Coats',
                             200000785: 'Tops & Tees', 100003141: 'Hoodies & Sweatshirts'},
        "Men's Clothing": {200216733: "Men's Sets", 200118008: 'Pants', 200000707: 'Tops & Tees',
                           200000709: 'Board Shorts',
                           200000701: 'Sweaters', 200000692: 'Suits & Blazers', 200000668: 'Shirts',
                           200000662: 'Jackets & Coats', 100003086: 'Jeans', 100003088: 'Casual Shorts',
                           100003084: 'Hoodies & Sweatshirts'},
        'Cellphones & Telecommunications': {200084017: 'Mobile Phone Accessories', 200086021: 'Mobile Phone Parts',
                                            200216959: 'Phone Bags & Cases',
                                            205668006: 'Walkie Talkie Parts & Accessories',
                                            200126001: 'Communication Equipments', 5090301: 'Cellphones',
                                            50906: 'Walkie Talkie', 205832906: 'Refurbished Phones',
                                            205838503: 'iPhones'},
        'Computer & Office': {200215304: 'Storage Devices', 702: 'Laptops', 703: 'Servers',
                              200216762: 'Demo Board & Accessories', 200216621: 'Tablets',
                              200216562: 'Computer Cables & Connectors', 70803003: 'Mini PC',
                              200002342: 'Computer Peripherals', 200002361: 'Tablet Accessories',
                              200002320: 'Networking',
                              200002319: 'Computer Components', 708022: 'Device Cleaners',
                              200004720: 'Office Electronics',
                              100005089: 'Industrial Computer & Accessories', 100005085: 'Mouse & Keyboards',
                              100005063: 'Laptop Accessories', 205848303: 'Laptop Parts', 205845408: 'Tablet Parts'},
        'Education & Office Supplies': {200003196: 'Writing & Correction Supplies', 205953922: 'Stationery Sticker',
                                        100003745: 'Notebooks & Writing Pads',
                                        100003836: 'Tapes, Adhesives & Fasteners',
                                        211106: 'Desk Accessories & Organizer',
                                        100005094: 'School & Educational Supplies',
                                        200003197: 'Labels, Indexes & Stamps', 205954820: 'Books & Magazines',
                                        211111: 'Art Supplies', 100003804: 'Filing Products',
                                        200003238: 'Mail & Shipping Supplies', 200003198: 'Calendars, Planners & Cards',
                                        100003809: 'Office Binding Supplies', 100003819: 'Cutting Supplies',
                                        212002: 'Presentation Supplies', 2112: 'Paper'},
        'Security & Protection': {200215432: 'Security Alarm', 200215427: 'Building Automation',
                                  200215424: 'Smart Card System', 200215419: 'Door Intercom',
                                  3007: 'Workplace Safety Supplies', 3009: 'Fire Protection',
                                  3011: 'Video Surveillance',
                                  3012: 'Safes', 3019: 'Self Defense Supplies', 3030: 'Access Control',
                                  205718021: 'Public Broadcasting', 200216744: 'Roadway Safety',
                                  200216754: 'Transmission & Cables', 205662015: 'IoT Devices',
                                  205676017: 'Security Inspection Device', 300912: 'Lightning Protection',
                                  200003251: 'Emergency Kits'},
        'Consumer Electronics': {200215272: 'VR/AR Devices', 200217534: 'Speakers',
                                 200216648: 'Sports & Action Video Cameras', 200216623: 'Earphones & Headphones',
                                 200216592: '360° Video Cameras & Accessories',
                                 200216598: 'Home Electronic Accessories',
                                 200218547: 'Power Source', 200218521: 'Live Equipment', 200217800: 'HIFI Devices',
                                 200217794: 'Robot', 200084019: 'Wearable Devices', 200002396: 'Video Games',
                                 200002395: 'Camera & Photo', 200002394: 'Accessories & Parts',
                                 200002398: 'Portable Audio & Video', 200002397: 'Home Audio & Video',
                                 200010196: 'Smart Electronics'},
        'Jewelry & Accessories': {200154003: 'Beads & Jewelry Making', 205871206: 'Jewelry making',
                                  205952104: 'Customized Jewelry', 200188001: 'Fine Jewelry',
                                  200000161: 'Wedding & Engagement Jewelry', 200000139: 'Earrings',
                                  200000109: 'Necklaces & Pendants', 200000097: 'Bracelets & Bangles',
                                  200132001: 'Jewelry Sets & More', 100006749: 'Rings'},
        'Watches': {200214074: "Women's Bracelet Watches", 200214047: "Lover's Watches",
                    200214043: "Children's Watches",
                    200214036: "Women's Watches", 200214006: "Men's Watches", 361120: 'Pocket & Fob Watches',
                    200000084: 'Watch Accessories'},
        'Home & Garden': {125: 'Garden Supplies', 200215281: 'Household Merchandises', 405: 'Home Textile',
                          1541: 'Home Storage & Organization', 3710: 'Home Decor', 200154001: 'Arts,Crafts & Sewing',
                          200002086: 'Kitchen,Dining & Bar', 200003136: 'Household Cleaning',
                          100002992: 'Festive & Party Supplies', 100004814: 'Bathroom Products',
                          100006206: 'Pet Products'},
        'Pet Products': {200216511: 'Insect Supplies', 200215873: 'GPS Trackers', 200215853: 'Dog Training Aids',
                         200215848: 'Dog Litter & Housebreaking', 200215847: 'Dog Collars & Leads',
                         200215838: 'Small Animal Supplies', 200217383: 'Pet Thermometers',
                         205658016: 'Pet Health Care & Hygiene', 200218061: 'Dog Doors, Houses & Furniture',
                         200218056: 'Dog Grooming', 200217967: 'Pet Microchips', 200217942: 'Pet Memorials',
                         205664011: 'Dog Food', 200036008: 'Dog Clothing & Shoes', 205680008: 'Pet Medical Supplies',
                         200002064: 'Bird Supplies', 200002071: 'Cat Supplies',
                         200002921: 'Reptile & Amphibian Supplies',
                         200002889: 'Dog Feeding', 200002896: 'Farm Animal Supplies', 200002893: 'Dog Toys',
                         200002886: 'Dog Carriers', 200002906: 'Fish & Aquatic Supplies'},
        'Home Appliances': {200214052: 'Household Appliances', 200214073: 'Personal Care Appliances',
                            200217027: 'Commercial Appliances', 200217594: 'Major Appliances',
                            100000016: 'Home Appliance Parts', 100000011: 'Kitchen Appliances'},
        'Luggage & Bags': {3803: 'Coin Purses & Holders', 152404: 'Luggage & Travel Bags',
                           152409: 'Bag Parts & Accessories', 152401: 'Backpacks', 152405: 'Wallets',
                           200068019: 'Functional Bags', 200066014: "Kids & Baby's Bags", 200010057: "Men's Bags",
                           200010063: "Women's Bags"},
        'Shoes': {100001606: "Women's Shoes", 200216407: "Women's Boots", 200002161: "Women's Pumps",
                  100001615: "Men's Shoes", 200002136: "Men's Casual Shoes", 200002164: "Women's Vulcanize Shoes",
                  200002124: 'Shoe Accessories', 200002155: "Women's Flats", 200002253: "Men's Vulcanize Shoes",
                  200216391: "Men's Boots"},
        'Toys & Hobbies': {200216936: 'Stress Relief Toy', 200218444: 'Pools & Water Fun',
                           200218343: 'Hobby & Collectibles', 200218367: 'Stuffed Animals & Plush',
                           200218357: 'Arts & Crafts, DIY toys', 200218333: 'High Tech Toys', 200218291: "Kid's Party",
                           200218269: 'Building & Construction Toys', 206081903: 'Play Vehicles & Models',
                           206089103: 'Ride On Toys', 206086301: 'Action & Toy Figures', 200003226: 'Puzzles & Games',
                           200003225: 'Dolls & Accessories', 200002636: 'Novelty & Gag Toys',
                           200002633: 'Model Building',
                           200002639: 'Remote Control Toys', 100001663: 'Diecasts & Toy Vehicles',
                           100001622: 'Baby & Toddler Toys', 100001624: 'Pretend Play',
                           100001623: 'Outdoor Fun & Sports',
                           100001629: 'Electronic Toys', 100001626: 'Classic Toys', 100001625: 'Learning & Education'},
        'Mother & Kids': {200217552: 'Baby Stroller & Accessories', 200217567: 'Toilet Training',
                          200217523: 'Car Seats & Accessories', 200217581: 'Pregnancy & Maternity',
                          200217580: 'Baby Souvenirs', 200217573: 'Baby Furniture',
                          200166001: 'Matching Family Outfits',
                          205870202: 'kids&Baby Accessories', 32212: "Children's Shoes", 200002433: 'Nappy Changing',
                          200002101: 'Baby Shoes', 200000567: "Girls' Baby Clothing", 200000528: "Boys' Baby Clothing",
                          200003595: 'Feeding', 200003594: 'Activity & Gear', 200003592: 'Safety Equipment',
                          100001118: 'Baby Care', 100003186: "Boys' Clothing", 100003199: "Girls' Clothing",
                          100002964: 'Baby Bedding'},
        'Sports & Entertainment': {200214370: 'Sports Accessories', 200217620: 'Sports Bags', 200094001: 'Team Sports',
                                   200001095: 'Sports Clothing', 200001115: 'Swimming', 200003570: 'Cycling',
                                   200005276: 'Sneakers', 200005156: 'Running',
                                   200005143: 'Roller Skates, Skateboards & Scooters', 200005102: 'Bowling',
                                   200005101: 'Entertainment', 200005059: 'Racquet Sports', 100005322: 'Golf',
                                   100005259: 'Fitness & Body Building', 100005575: 'Water Sports',
                                   100005471: 'Hunting',
                                   100005444: 'Fishing', 100005433: 'Camping & Hiking',
                                   100005383: 'Musical Instruments'},
        'Beauty & Health': {3305: 'Oral Hygiene', 3306: 'Skin Care', 660103: 'Makeup', 660302: 'Shaving & Hair Removal',
                            200002496: 'Health Care', 200002444: 'Bath & Shower', 200002458: 'Hair Care & Styling',
                            200002454: 'Fragrances & Deodorants', 200003551: 'Tattoo & Body Art',
                            200003045: 'Sex Products',
                            200002569: 'Tools & Accessories', 200002547: 'Nails Art & Tools',
                            201902009: "Men's Grooming",
                            205778203: 'Skin Care Tools', 200074001: 'Beauty Essentials'},
        'Hair Extensions & Wigs': {200218141: 'Human Hair Weaves', 200217672: 'Synthetic Extensions',
                                   200217671: 'Hair Braids', 200217666: 'Synthetic Wigs',
                                   200217696: 'Salon Hair Supply Chain', 200217614: 'Hair Extensions',
                                   200002956: 'Hair Salon Tools & Accessories', 200004346: 'Lace Wigs',
                                   200004940: 'Hair Pieces'},
        'Automobiles & Motorcycles': {200216084: 'Car Lights', 200216017: 'Car Repair Tools',
                                      200214451: 'ATV,RV,Boat & Other Vehicle', 200217080: 'Travel & Roadway Product',
                                      200217078: 'Car Wash & Maintenance', 200000408: 'Motorcycle Accessories & Parts',
                                      200000369: 'Car Electronics', 200000191: 'Auto Replacement Parts',
                                      200004620: 'Exterior Accessories', 200004619: 'Interior Accessories'},
        'Tools': {1417: 'Power Tools', 1427: 'Welding & Soldering Supplies', 1428: 'Abrasives',
                  1431: 'Woodworking Machinery & Parts', 1440: 'Welding Equipment',
                  1537: 'Measurement & Analysis Instruments', 4204: 'Abrasive Tools', 200216862: 'Riveter Guns',
                  200218051: 'Hand & Power Tool Accessories', 200218021: 'Lifting Tools & Accessories',
                  142003: 'Hand Tools', 142001: 'Tool Parts', 142016: 'Construction Tools', 12503: 'Garden Tools',
                  100006919: 'Tool Sets', 100006925: 'Tool Organizers', 100006799: 'Machine Tools & Accessories'},
        'Home Improvement': {5: 'Electrical Equipments & Supplies', 42: 'Hardware', 200215252: 'Kitchen Fixtures',
                             200217293: 'Plumbing', 200217241: 'Painting Supplies & Wall Treatments',
                             200217718: 'Family Intelligence System', 39: 'Lights & Lighting',
                             200003230: 'Building Supplies', 100006479: 'Bathroom Fixtures'}}
    global addData
    addData = {
        'item_url': [],
        'sale_num': [],
        'imageurl': [],
        'productId': [],
        'storeUrl': [],
        'aliMemberId': [],
        'storeName': [],
        'storeId': [],
        'displayTitle': [],
        'seoTitle': [],
        'clickurl': [],
        'lunchTime': [],
        'builderType': [],
        'taxRate': [],
        'pricesStyle': [],
        'formatted_price2': [],
        'minPriceDiscount': [],
        'cent_price': [],
        'minPrice': [],
        'priceType': [],
        'discount': [],
        'currencyCode': [],
        'productType': [],
        'sellingPoints': [],
    }
    for childCategories_dict in dict.values():
        thread_list = []
        for id, value in childCategories_dict.items():
            value = value.replace(' & ', '-')
            value = value.replace(' ', '-')
            child_url = f'https://www.aliexpress.com/category/{id}/{value}.html'
            # 每一个子类目，第一页数据
            # print(child_url)
            t = threading.Thread(target=crawl_thread,
                                 args=(child_url, id))
            t.start()
            thread_list.append(t)

        for t in thread_list:
            t.join()

    save_to_csv(filename='AE_items.csv', data=addData)


process_data()
