from linkcleaner.utils import clean_url

TESTCASES = {
    # Amazon
    "https://www.amazon.ca/Fire-HD-8-Tablet/dp/B07WFKKN55?ref=dlx_boxin_gd_dcl_img_0_25e298cd_dt_sl10_10#compare": "https://www.amazon.ca/Fire-HD-8-Tablet/dp/B07WFKKN55#compare",
    "https://www.amazon.ca/events/boxingday?pf_rd_r=SRMTVF5TW3T72BBBQ329&pf_rd_p=64caa6c6-08cf-463b-9628-8992208d1ceb&pd_rd_r=feb3ac41-db02-42c0-ad25-f69a35fc2931&pd_rd_w=wTHSV&pd_rd_wb=doNPo&ref_=pd_gw_unk": "https://www.amazon.ca/events/boxingday",
    "https://www.amazon.com/b?node=16225007011&pf_rd_r=BSW1FBWQ7QM7JK7S8AMY&pf_rd_p=e5b0c85f-569c-4c90-a58f-0c0a260e45a0&pd_rd_r=94a55ac8-8cfc-4e5d-a605-e0dc6a04a0a5&pd_rd_w=GgmXK&pd_rd_wg=J0PSu&ref_=pd_gw_unk": "https://www.amazon.com/b?node=16225007011",
    "https://www.amazon.com/Seagate-Portable-External-Hard-Drive/dp/B07CRG94G3/ref=lp_16225507011_1_3": "https://www.amazon.com/Seagate-Portable-External-Hard-Drive/dp/B07CRG94G3/",

    # Twitter
    "https://twitter.com/PlanNorge/status/1181537299038953473?ref_src=twsrc%2525255Etfw%2525257Ctwcamp%2525255Etweetembed%2525257Ctwterm%2525255E1181537299038953473&ref_url=https%2525253A%2525252F%2525252Fwww.vg.no%2525252F": "https://twitter.com/PlanNorge/status/1181537299038953473",

    "https://www.example.com/page?utm_content=buffercf3b2&utm_medium=social&utm_source=facebook.com&utm_campaign=buffer": "https://www.example.com/page",
}


def test_cleaning():
    for k, v in TESTCASES.items():
        assert clean_url(k) == v
