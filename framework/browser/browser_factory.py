from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from resources import config


def get_driver() -> webdriver:
    if config.BROWSER == "chrome":
        return webdriver.Chrome(ChromeDriverManager().install(),
                                options=get_browser_options(config.BROWSER))
    elif config.BROWSER == "firefox":
        return webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                 options=get_browser_options(config.BROWSER))
    else:
        raise ValueError("Unknown browser")


def get_browser_options(browser):
    if browser == "chrome":
        chrome_options = webdriver.ChromeOptions()
        prefs = {"intl.accept_languages": str(config.LANGUAGE)}
        chrome_options.add_experimental_option("prefs", prefs)
        return chrome_options
    elif browser == "firefox":
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_preference("intl.accept_languages", str(config.LANGUAGE))
        return firefox_options
