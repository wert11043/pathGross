const data = window.PATH_GROSS_DATA || { title: "Path Gross Flashcards", subtitle: "", groups: [], cards: [] };
const STORAGE_KEY = "pathGrossCardStatus.v1";
const REVISIT_OFFSET = 4;
const SWIPE_THRESHOLD = 110;

const state = {
  pool: new Set(),
  group: "all",
  deck: [],
  current: null,
  revealed: false,
  showSource: false,
  drag: {
    active: false,
    pointerId: null,
    startX: 0,
    deltaX: 0
  },
  progressMap: loadProgress(),
  sessionRated: 0,
  sessionStartSize: 0
};

const poolOptions = [
  { key: "all", label: "All" },
  { key: "new", label: "Unmarked" },
  { key: "unknown", label: "Unfamiliar" },
  { key: "known", label: "Familiar" }
];

const elements = {
  pageTitle: document.getElementById("pageTitle"),
  pageSubtitle: document.getElementById("pageSubtitle"),
  poolChips: document.getElementById("poolChips"),
  groupChips: document.getElementById("groupChips"),
  remainingCount: document.getElementById("remainingCount"),
  knownCount: document.getElementById("knownCount"),
  unknownCount: document.getElementById("unknownCount"),
  positionCount: document.getElementById("positionCount"),
  shuffleBtn: document.getElementById("shuffleBtn"),
  toggleMaskBtn: document.getElementById("toggleMaskBtn"),
  resetProgressBtn: document.getElementById("resetProgressBtn"),
  flashcard: document.getElementById("flashcard"),
  imageFrame: document.getElementById("imageFrame"),
  imageGallery: document.getElementById("imageGallery"),
  cardGroup: document.getElementById("cardGroup"),
  cardPage: document.getElementById("cardPage"),
  hintLine: document.getElementById("hintLine"),
  answerPanel: document.getElementById("answerPanel"),
  cardAnswer: document.getElementById("cardAnswer"),
  cardOrgan: document.getElementById("cardOrgan"),
  revealBtn: document.getElementById("revealBtn"),
  unknownBtn: document.getElementById("unknownBtn"),
  knownBtn: document.getElementById("knownBtn"),
  leftBadge: document.getElementById("leftBadge"),
  rightBadge: document.getElementById("rightBadge"),
  emptyStateCard: document.getElementById("emptyStateCard")
};

function loadProgress() {
  try {
    return JSON.parse(window.localStorage.getItem(STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

function saveProgress() {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state.progressMap));
}

function shuffle(items) {
  const copy = [...items];
  for (let index = copy.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
  }
  return copy;
}

function countByStatus(status) {
  return data.cards.filter((card) => state.progressMap[card.id] === status).length;
}

function getCardStatus(card) {
  return state.progressMap[card.id] || "new";
}

function matchesPool(card) {
  const status = getCardStatus(card);
  if (state.pool.size === 0) return true;
  return state.pool.has(status);
}

function matchesGroup(card) {
  return state.group === "all" || card.group === state.group;
}

function buildDeck() {
  const filtered = data.cards.filter((card) => matchesPool(card) && matchesGroup(card));
  state.deck = shuffle(filtered);
  state.current = state.deck[0] || null;
  state.revealed = false;
  state.sessionRated = 0;
  state.sessionStartSize = state.deck.length;
}

function renderChips(container, options, isActive, onSelect) {
  container.innerHTML = "";
  options.forEach((option) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `chip${isActive(option.key) ? " is-active" : ""}`;
    button.textContent = option.label;
    button.addEventListener("click", () => onSelect(option.key));
    container.appendChild(button);
  });
}

function renderFilters() {
  renderChips(elements.poolChips, poolOptions, (key) => {
    if (key === "all") {
      return state.pool.size === 0;
    }
    return state.pool.has(key);
  }, (key) => {
    if (key === "all") {
      state.pool.clear();
      rebuildAndRender();
      return;
    }

    if (state.pool.has(key)) {
      state.pool.delete(key);
    } else {
      state.pool.add(key);
    }
    rebuildAndRender();
  });

  const groupOptions = [{ key: "all", label: "All systems" }, ...data.groups.map((group) => ({ key: group, label: group }))];
  renderChips(elements.groupChips, groupOptions, (key) => key === state.group, (key) => {
    state.group = key;
    rebuildAndRender();
  });
}

function setButtonState(disabled) {
  [elements.revealBtn, elements.unknownBtn, elements.knownBtn, elements.shuffleBtn, elements.toggleMaskBtn].forEach((button) => {
    button.disabled = disabled;
    button.style.opacity = disabled ? "0.5" : "1";
    button.style.cursor = disabled ? "not-allowed" : "pointer";
  });
}

function getCardImages(card) {
  if (Array.isArray(card.images) && card.images.length > 0) {
    return card.images;
  }
  if (card.image) {
    return [card.image];
  }
  return [];
}

function renderGallery(card) {
  const images = getCardImages(card);
  elements.imageGallery.innerHTML = "";
  elements.imageGallery.dataset.count = String(images.length);

  images.forEach((src, index) => {
    const tile = document.createElement("figure");
    tile.className = "image-tile";

    const image = document.createElement("img");
    image.src = src;
    image.alt = `Gross specimen image ${index + 1} for page ${card.page}`;
    tile.appendChild(image);

    const topMask = document.createElement("div");
    topMask.className = "label-mask top";
    tile.appendChild(topMask);

    const bottomMask = document.createElement("div");
    bottomMask.className = "label-mask bottom";
    tile.appendChild(bottomMask);

    elements.imageGallery.appendChild(tile);
  });
}

function renderStats() {
  elements.remainingCount.textContent = String(state.deck.length);
  elements.knownCount.textContent = String(countByStatus("known"));
  elements.unknownCount.textContent = String(countByStatus("unknown"));

  if (!state.current) {
    elements.positionCount.textContent = "0 / 0";
    return;
  }

  const currentSlot = Math.min(state.sessionRated + 1, Math.max(state.sessionStartSize, 1));
  elements.positionCount.textContent = `${currentSlot} / ${Math.max(state.sessionStartSize, 1)}`;
}

function renderCard() {
  const card = state.current;

  if (!card) {
    elements.cardGroup.textContent = "No cards";
    elements.cardPage.textContent = "Page -";
    elements.imageGallery.innerHTML = "";
    elements.imageGallery.dataset.count = "0";
    elements.answerPanel.classList.add("is-hidden");
    elements.flashcard.classList.remove("is-revealed");
    elements.hintLine.textContent = "Change the review pool or system filter to keep studying.";
    elements.emptyStateCard.classList.add("is-visible");
    setButtonState(true);
    return;
  }

  elements.emptyStateCard.classList.remove("is-visible");
  setButtonState(false);
  elements.cardGroup.textContent = card.group;
  elements.cardPage.textContent = `Page ${card.page}`;
  renderGallery(card);
  elements.cardAnswer.textContent = card.answer;
  elements.cardOrgan.textContent = `${card.organ} - Page ${card.page}`;
  elements.imageFrame.classList.toggle("show-source", state.showSource);
  elements.toggleMaskBtn.textContent = state.showSource ? "Cover Labels Again" : "Show Full Images";

  if (state.revealed) {
    elements.flashcard.classList.add("is-revealed");
    elements.answerPanel.classList.remove("is-hidden");
    elements.hintLine.textContent = "Swipe or use the buttons to mark familiar / unfamiliar.";
    elements.revealBtn.textContent = "Diagnosis Revealed";
  } else {
    elements.flashcard.classList.remove("is-revealed");
    elements.answerPanel.classList.add("is-hidden");
    elements.hintLine.textContent = "Tap the card or press space to reveal the diagnosis.";
    elements.revealBtn.textContent = "Reveal Diagnosis";
  }
}

function render() {
  elements.pageTitle.textContent = data.title;
  elements.pageSubtitle.textContent = data.subtitle;
  renderFilters();
  renderStats();
  renderCard();
}

function rebuildAndRender() {
  buildDeck();
  render();
}

function revealAnswer() {
  if (!state.current || state.revealed) return;
  state.revealed = true;
  renderCard();
}

function nextCard() {
  state.current = state.deck[0] || null;
  state.revealed = false;
  resetCardTransform();
  renderStats();
  renderCard();
  elements.flashcard.focus();
}

function rateCard(status) {
  if (!state.current) return;
  if (!state.revealed) {
    revealAnswer();
    return;
  }

  const currentCard = state.deck.shift();
  state.progressMap[currentCard.id] = status;
  saveProgress();

  if (status === "unknown") {
    const insertIndex = Math.min(REVISIT_OFFSET, state.deck.length);
    state.deck.splice(insertIndex, 0, currentCard);
  }

  state.sessionRated += 1;
  nextCard();
}

function resetCardTransform() {
  state.drag.active = false;
  state.drag.pointerId = null;
  state.drag.deltaX = 0;
  elements.flashcard.classList.remove("is-dragging");
  elements.flashcard.style.transform = "";
  elements.leftBadge.classList.remove("is-visible");
  elements.rightBadge.classList.remove("is-visible");
}

function updateSwipeVisual(deltaX) {
  const rotation = deltaX / 26;
  elements.flashcard.style.transform = `translateX(${deltaX}px) rotate(${rotation}deg)`;
  elements.leftBadge.classList.toggle("is-visible", deltaX < -30);
  elements.rightBadge.classList.toggle("is-visible", deltaX > 30);
}

function onPointerDown(event) {
  if (!state.current || !state.revealed) return;
  state.drag.active = true;
  state.drag.pointerId = event.pointerId;
  state.drag.startX = event.clientX;
  state.drag.deltaX = 0;
  elements.flashcard.classList.add("is-dragging");
  elements.flashcard.setPointerCapture(event.pointerId);
}

function onPointerMove(event) {
  if (!state.drag.active || event.pointerId !== state.drag.pointerId) return;
  state.drag.deltaX = event.clientX - state.drag.startX;
  updateSwipeVisual(state.drag.deltaX);
}

function onPointerUp(event) {
  if (!state.drag.active || event.pointerId !== state.drag.pointerId) return;
  const deltaX = state.drag.deltaX;
  resetCardTransform();
  if (deltaX <= -SWIPE_THRESHOLD) {
    rateCard("unknown");
    return;
  }
  if (deltaX >= SWIPE_THRESHOLD) {
    rateCard("known");
  }
}

function handleKeyboard(event) {
  if (event.target && ["INPUT", "TEXTAREA", "SELECT", "BUTTON"].includes(event.target.tagName)) {
    return;
  }

  if (event.code === "Space") {
    event.preventDefault();
    revealAnswer();
    return;
  }

  if (event.key === "ArrowLeft") {
    event.preventDefault();
    rateCard("unknown");
    return;
  }

  if (event.key === "ArrowRight") {
    event.preventDefault();
    rateCard("known");
    return;
  }

  if (event.key.toLowerCase() === "r") {
    event.preventDefault();
    state.deck = shuffle(state.deck);
    state.current = state.deck[0] || null;
    state.revealed = false;
    renderStats();
    renderCard();
  }
}

elements.flashcard.addEventListener("click", () => {
  revealAnswer();
});

elements.flashcard.addEventListener("pointerdown", onPointerDown);
elements.flashcard.addEventListener("pointermove", onPointerMove);
elements.flashcard.addEventListener("pointerup", onPointerUp);
elements.flashcard.addEventListener("pointercancel", resetCardTransform);
elements.flashcard.addEventListener("lostpointercapture", resetCardTransform);

elements.revealBtn.addEventListener("click", revealAnswer);
elements.unknownBtn.addEventListener("click", () => rateCard("unknown"));
elements.knownBtn.addEventListener("click", () => rateCard("known"));

elements.shuffleBtn.addEventListener("click", () => {
  state.deck = shuffle(state.deck);
  state.current = state.deck[0] || null;
  state.revealed = false;
  renderStats();
  renderCard();
});

elements.toggleMaskBtn.addEventListener("click", () => {
  state.showSource = !state.showSource;
  renderCard();
});

elements.resetProgressBtn.addEventListener("click", () => {
  if (!window.confirm("Reset all familiar / unfamiliar marks?")) return;
  state.progressMap = {};
  saveProgress();
  rebuildAndRender();
});

window.addEventListener("keydown", handleKeyboard);

buildDeck();
render();
