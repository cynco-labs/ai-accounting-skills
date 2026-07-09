/** Client interactions — mirrored from opencode.ai/data shell behaviour */

const THEME_KEY = "opencode:stats-theme"
type ThemePreference = "dark" | "light" | "system"

function isThemePreference(value: string | null): value is ThemePreference {
  return value === "dark" || value === "light" || value === "system"
}

function applyThemePreference(preference: ThemePreference) {
  document.documentElement.dataset.statsTheme = preference
  if (preference === "system") document.documentElement.style.removeProperty("color-scheme")
  else document.documentElement.style.setProperty("color-scheme", preference)

  document.querySelectorAll<HTMLButtonElement>("[data-theme-value]").forEach((btn) => {
    const active = btn.getAttribute("data-theme-value") === preference
    btn.setAttribute("aria-pressed", active ? "true" : "false")
  })
}

function initTheme() {
  let preference: ThemePreference = "system"
  try {
    const stored = localStorage.getItem(THEME_KEY)
    if (isThemePreference(stored)) preference = stored
  } catch {
    /* ignore */
  }
  applyThemePreference(preference)

  document.querySelectorAll<HTMLButtonElement>("[data-theme-value]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const next = btn.getAttribute("data-theme-value")
      if (!isThemePreference(next)) return
      applyThemePreference(next)
      try {
        localStorage.setItem(THEME_KEY, next)
      } catch {
        /* ignore */
      }
    })
  })
}

function initTabs() {
  document.querySelectorAll("[data-component-tabs], [data-component='install-panel']").forEach((tabsRoot) => {
    const tabs = tabsRoot.querySelectorAll<HTMLElement>("[data-tab]")
    const panels = tabsRoot.querySelectorAll<HTMLElement>("[data-panel]")
    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const id = tab.getAttribute("data-tab")
        tabs.forEach((t) => t.setAttribute("aria-selected", t === tab ? "true" : "false"))
        panels.forEach((p) => {
          if (p.getAttribute("data-panel") === id) p.setAttribute("data-active", "")
          else p.removeAttribute("data-active")
        })
        tabsRoot.setAttribute("data-active", id || "")
      })
    })
  })
}

async function copyText(text: string) {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    const ta = document.createElement("textarea")
    ta.value = text
    ta.style.position = "fixed"
    ta.style.left = "-9999px"
    document.body.appendChild(ta)
    ta.select()
    try {
      document.execCommand("copy")
      return true
    } finally {
      document.body.removeChild(ta)
    }
  }
}

function initCopy() {
  document.querySelectorAll<HTMLElement>("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const text = btn.getAttribute("data-copy") || ""
      if (!(await copyText(text))) return
      btn.setAttribute("data-copied", "")
      window.setTimeout(() => btn.removeAttribute("data-copied"), 1500)
    })
  })
}

function setFaqOpen(item: Element, open: boolean) {
  const trigger = item.querySelector<HTMLElement>("[data-slot='faq-question']")
  const plus = item.querySelector<HTMLElement>(".icon-plus")
  const minus = item.querySelector<HTMLElement>(".icon-minus")
  if (open) {
    item.setAttribute("data-expanded", "")
    trigger?.setAttribute("aria-expanded", "true")
    if (plus) plus.style.display = "none"
    if (minus) minus.style.display = ""
  } else {
    item.removeAttribute("data-expanded")
    trigger?.setAttribute("aria-expanded", "false")
    if (plus) plus.style.display = ""
    if (minus) minus.style.display = "none"
  }
}

function initFaq() {
  document.querySelectorAll("[data-faq-item]").forEach((item) => {
    const trigger = item.querySelector("[data-slot='faq-question']")
    if (!trigger) return
    trigger.addEventListener("click", () => {
      const open = item.hasAttribute("data-expanded")
      document.querySelectorAll("[data-faq-item][data-expanded]").forEach((other) => {
        if (other !== item) setFaqOpen(other, false)
      })
      setFaqOpen(item, !open)
    })
  })
}

function initMobileNav() {
  const header = document.querySelector('[data-component="top"]')
  const toggle = document.querySelector('[data-component="nav-mobile-toggle"]')
  const mobile = document.querySelector('[data-component="nav-mobile"]')
  if (!toggle || !mobile) return

  const setOpen = (open: boolean) => {
    if (open) {
      mobile.removeAttribute("hidden")
      header?.setAttribute("data-menu-open", "true")
      toggle.setAttribute("aria-expanded", "true")
      toggle.setAttribute("aria-label", "Close navigation")
      document.body.style.overflow = "hidden"
      toggle.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M4.44 4.44L11.56 11.56M11.56 4.44L4.44 11.56" stroke="currentColor"></path></svg>'
    } else {
      mobile.setAttribute("hidden", "")
      header?.removeAttribute("data-menu-open")
      toggle.setAttribute("aria-expanded", "false")
      toggle.setAttribute("aria-label", "Open navigation")
      document.body.style.overflow = ""
      toggle.innerHTML =
        '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true"><path d="M2 4.72H14M2 8.5H14M2 12.28H14" stroke="currentColor"></path></svg>'
    }
  }

  toggle.addEventListener("click", () => {
    setOpen(mobile.hasAttribute("hidden"))
  })
  mobile.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setOpen(false)))
}

function initYear() {
  const year = document.getElementById("year")
  if (year) year.textContent = String(new Date().getFullYear())
}

function initLanding() {
  initYear()
  initTheme()
  initTabs()
  initCopy()
  initFaq()
  initMobileNav()
}

initLanding()
