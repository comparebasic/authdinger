from playwright.sync_api import Page, Playwright, sync_playwright, expect
from . import fixtures

def test_has_title(page: Page):
    page.goto("http://localhost:3000")

    expect(page).to_have_title("PolyVinyl Example  - Login or Sign Up")

def test_login(page: Page):
    user = fixtures.get_user("testone")
    fixtures.wipe_user(user)

    page.goto("http://localhost:3000/auth/login")
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill(user["email"])
    page.get_by_text("Login or Create Account").click()
    page.get_by_text("Use password").click()
    page.get_by_role("textbox", name="Password 👁").click()
    page.get_by_role("textbox", name="Password 👁").fill(user["password"])
    page.get_by_text("Register new user").click()
    page.get_by_role("textbox", name="Fullname Sign up for our").click()
    page.get_by_role("textbox", name="Fullname Sign up for our").fill(user["fullname"])
    page.get_by_text("Sign up for our Newsletters").click()
    page.get_by_text("Products and features").nth(1).click()
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("heading", name="Dashboard").click()
    page.get_by_text("Hi, {} ({})".format(user["fullname"], user["email"])).click()
    page.get_by_role("link", name="logout", exact=True).click()
    page.get_by_text("Login or Sign Up").click()

    # relogin
    page.get_by_text("Login or Create Account").click()
    page.get_by_role("textbox", name="Email").click()
    page.get_by_role("textbox", name="Email").fill(user["email"])
    page.get_by_text("Use password").click()
    page.get_by_role("textbox", name="Password 👁").click()
    page.get_by_role("textbox", name="Password 👁").fill(user["password"])
    page.get_by_role("button", name="Submit").click()
    page.get_by_role("heading", name="Dashboard").click()
    page.get_by_text("Hi, {} ({})".format(user["fullname"], user["email"])).click()
    page.get_by_role("link", name="logout", exact=True).click()
    page.get_by_text("Login or Sign Up").click()
