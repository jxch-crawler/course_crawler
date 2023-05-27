#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
import KeStudy163CourseByYangLiang30 as detailPage
import logging


class TestWebsite:
    @pytest.fixture(autouse=True)
    def browser_setup_and_teardown(self):
        logging.basicConfig(level=logging.INFO)
        self.use_selenoid = False  # set to True to run tests with Selenoid

        if self.use_selenoid:
            self.browser = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities={
                    "browserName": "chrome",
                    "browserSize": "1920x1080"
                }
            )
        else:
            self.browser = webdriver.Chrome(
                executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

        self.browser.maximize_window()
        self.browser.implicitly_wait(10)
        self.page = detailPage.KeStudy163CourseByYangLiang30(self.browser)

        yield

        self.browser.close()
        self.browser.quit()

    def test(self):
        self.page.download()
