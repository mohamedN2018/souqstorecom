import { ref, onMounted, onUnmounted } from "vue";

/*
  Smart header behavior:
    • scrolling DOWN  → collapse the top rows (TopBar + Header), keep only NavBar
    • scrolling UP    → reveal everything again
    • near the top    → always fully expanded
  Returns `collapsed` (true = only the navbar should show).
*/
export function useHeaderScroll(threshold = 140) {
  const collapsed = ref(false);
  let last = 0;
  let ticking = false;

  function update() {
    const y = window.scrollY || 0;
    if (y < threshold) {
      collapsed.value = false; // always show the full header up top
    } else if (y > last + 6) {
      collapsed.value = true; // scrolling down
    } else if (y < last - 6) {
      collapsed.value = false; // scrolling up
    }
    last = y;
    ticking = false;
  }

  function onScroll() {
    if (!ticking) {
      ticking = true;
      window.requestAnimationFrame(update);
    }
  }

  onMounted(() => window.addEventListener("scroll", onScroll, { passive: true }));
  onUnmounted(() => window.removeEventListener("scroll", onScroll));

  return { collapsed };
}
