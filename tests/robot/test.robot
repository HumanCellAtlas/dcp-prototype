*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Library   Browser

*** Test Cases ***
Front Page For Average Joe
    New Page         https://cellxgene.staging.single-cell.czi.technology/
    Get Text         //*[@id="__next"]/div/div[2]/main/div/div/h1    contains    Collections
    Get Text         //*[@id="__next"]/div/div[2]/main/div    	not contains     Create Collection
	Get Text         //*[@id="__next"]/div/div[2]/main/table/tbody/tr[1]/td[1]/a
	${collection_url}=    Get Attribute    /*[@id="__next"]/div/div[2]/main/table/tbody/tr[1]/td[1]/a

Front Page For Curator
    New Page    https://cellxgene.staging.single-cell.czi.technology/?cc=true&auth=true
	Get Text    //*[@id="__next"]/div/div[1]/div/span/div/a/span    contains    Log In
    Get Text    //*[@id="__next"]/div/div[2]/main/div    	contains     Create Collection
