*** Settings ***
Documentation     A test suite with a single test for valid login.
...
...               This test has a workflow that is created using keywords in
...               the imported resource file.
Library   Browser

*** Test Cases ***
Example Test
    New Page    https://cellxgene.staging.single-cell.czi.technology/
    Get Text    h1    contains    Collections


