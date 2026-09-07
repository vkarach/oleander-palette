# -*- coding: utf-8 -*-
"""Build docs/index.html (the palette reference page) from a tdesktop-palette file.

Usage: python build.py [path/to/Oleander.tdesktop-palette]
Default input: palette/Oleander.tdesktop-palette
"""
import re, json, sys, os

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join("palette", "Oleander.tdesktop-palette")
TEMPLATE = "template.html"
OUT = os.path.join("docs", "index.html")

line_re = re.compile(r"^(\w+):\s*(#[0-9a-fA-F]{6,8}|\w+);(?:\s*//\s*(.*))?$")

raw, comment, const_order = {}, {}, []
in_consts = False
for ln in open(SRC, encoding="utf-8"):
    s = ln.strip()
    if s.startswith("// === OLEANDER CONSTANTS"):
        in_consts = True
        continue
    if in_consts and s.startswith("// ===="):
        in_consts = False
        continue
    m = line_re.match(ln)
    if not m:
        continue
    raw[m.group(1)] = m.group(2)
    comment[m.group(1)] = (m.group(3) or "").strip()
    if in_consts:
        const_order.append(m.group(1))


def resolve(key):
    v = raw[key]
    seen = set()
    while not v.startswith("#"):
        if v in seen:
            return "#000000"
        seen.add(v)
        v = raw[v]
    return v


CONST_LABELS = {
    "OLEANDER_BG": "Основной фон",
    "OLEANDER_BG_DEEP": "Самый тёмный фон (панель папок)",
    "OLEANDER_BG_OVER": "Фон под курсором",
    "OLEANDER_BG_RIPPLE": "Волна при клике",
    "OLEANDER_BG_PANEL": "Фон панелей и полей поиска",
    "OLEANDER_ACCENT": "Акцент (заливка активного)",
    "OLEANDER_ACCENT_DEEP": "Тёмный акцент (кнопки)",
    "OLEANDER_ACCENT_LIGHT": "Светлый акцент (ссылки, онлайн)",
    "OLEANDER_TEXT": "Основной текст",
    "OLEANDER_TEXT_SUB": "Второстепенный текст",
    "OLEANDER_BUBBLE_IN": "Входящий пузырь (непрозрачный)",
    "OLEANDER_BUBBLE_OUT": "Исходящий пузырь (непрозрачный)",
    "OLEANDER_BUBBLE_SEL": "Выделенное сообщение",
    "OLEANDER_COMPOSE_BG": "Поле ввода",
    "OLEANDER_COMPOSE_EDGE": "Рамка вокруг поля ввода",
    "OLEANDER_PANEL_85": "Панель Unmute / Join",
    "OLEANDER_ICON_85": "Скрепка, смайлик, микрофон",
    "OLEANDER_ICON_85_OVER": "Те же иконки под курсором",
    "OLEANDER_BUBBLE_IN_80": "Входящий пузырь",
    "OLEANDER_BUBBLE_OUT_80": "Исходящий пузырь",
    "OLEANDER_BUBBLE_IN_85": "Входящий пузырь",
    "OLEANDER_BUBBLE_OUT_85": "Исходящий пузырь",
}

GROUPS = [
 ("Константы темы", "Ручки. Меняешь строку здесь, меняются все ключи ниже.",
  [(k, CONST_LABELS.get(k, k)) for k in const_order]),
 ("Окно и общие цвета", "Фолбэки: ключ, который ты не задал явно, берёт цвет отсюда.", [
    ("windowBg", "Фон окна, он же фон списка чатов"),
    ("windowBgOver", "Фон элемента под курсором"),
    ("windowBgRipple", "Волна при клике"),
    ("windowFg", "Основной текст"),
    ("windowSubTextFg", "Второстепенный текст"),
    ("windowBoldFg", "Жирный текст"),
    ("windowBgActive", "Заливка активных областей"),
    ("windowFgActive", "Текст поверх активной заливки"),
    ("windowActiveTextFg", "Активный текст: ссылки, статус онлайн"),
    ("windowShadowFg", "Тень"),
    ("layerBg", "Затемнение под открытым окном"),
 ]),
 ("Заголовок окна", "Верхняя полоса с кнопками свернуть, развернуть, закрыть.", [
    ("titleBg", "Фон, когда окно неактивно"),
    ("titleBgActive", "Фон, когда окно активно"),
    ("titleButtonFg", "Иконки кнопок"),
    ("titleButtonFgOver", "Иконки под курсором"),
    ("titleButtonCloseBgOver", "Фон крестика под курсором"),
 ]),
 ("Панель папок слева", "Узкая колонка с All chats, Rust, News.", [
    ("sideBarBg", "Фон панели"),
    ("sideBarBgActive", "Фон активной папки"),
    ("sideBarBgRipple", "Волна при клике"),
    ("sideBarTextFg", "Подпись папки"),
    ("sideBarTextFgActive", "Подпись активной папки"),
    ("sideBarIconFg", "Иконка папки"),
    ("sideBarIconFgActive", "Иконка активной папки"),
    ("sideBarBadgeBg", "Счётчик непрочитанных"),
    ("sideBarBadgeBgMuted", "Счётчик для замьюченных"),
 ]),
 ("Список чатов", "Левая колонка со строками чатов и поиском.", [
    ("dialogsBg", "Фон списка"),
    ("dialogsBgOver", "Строка под курсором"),
    ("dialogsBgActive", "Строка открытого чата"),
    ("dialogsRippleBg", "Волна при клике по строке"),
    ("dialogsNameFg", "Название чата"),
    ("dialogsNameFgActive", "Название в открытом чате"),
    ("dialogsTextFg", "Текст последнего сообщения"),
    ("dialogsTextFgService", "Имя отправителя в группе"),
    ("dialogsDateFg", "Время справа"),
    ("dialogsDraftFg", "Метка Draft"),
    ("dialogsUnreadBg", "Счётчик непрочитанных"),
    ("dialogsUnreadBgMuted", "Счётчик у замьюченного чата"),
    ("dialogsUnreadFg", "Цифра в счётчике"),
    ("dialogsOnlineBadgeFg", "Зелёная точка онлайн"),
    ("dialogsSentIconFg", "Галочки отправлено, прочитано"),
    ("dialogsVerifiedIconBg", "Значок верификации"),
    ("searchedBarBg", "Полоса заголовка результатов поиска"),
    ("searchedBarFg", "Текст в этой полосе"),
    ("filterInputInactiveBg", "Поле поиска, неактивное"),
    ("filterInputActiveBg", "Поле поиска, активное"),
 ]),
 ("Верх чата", "Шапка с именем собеседника и закреплённое сообщение.", [
    ("topBarBg", "Фон шапки чата"),
    ("historyPinnedBg", "Полоса закреплённого сообщения"),
    ("historyUnreadBarBg", "Полоса Unread messages"),
    ("historyUnreadBarFg", "Текст в этой полосе"),
 ]),
 ("Сообщения", "Пузыри, текст в них и всё, что внутри.", [
    ("msgInBg", "Входящий пузырь"),
    ("msgInBgSelected", "Входящий выделенный"),
    ("msgOutBg", "Исходящий пузырь"),
    ("msgOutBgSelected", "Исходящий выделенный"),
    ("historyTextInFg", "Текст входящего"),
    ("historyTextOutFg", "Текст исходящего"),
    ("msgInDateFg", "Время во входящем"),
    ("msgOutDateFg", "Время в исходящем"),
    ("historyLinkInFg", "Ссылка во входящем"),
    ("historyLinkOutFg", "Ссылка в исходящем"),
    ("msgInMonoFg", "Моноширинный текст, входящий"),
    ("msgOutMonoFg", "Моноширинный текст, исходящий"),
    ("msgInReplyBarColor", "Полоска цитаты во входящем"),
    ("msgOutReplyBarColor", "Полоска цитаты в исходящем"),
    ("msgInServiceFg", "Служебный текст во входящем"),
    ("msgOutServiceFg", "Служебный текст в исходящем"),
    ("historyOutIconFg", "Галочки на исходящем"),
    ("msgServiceBg", "Плашка даты и служебных сообщений"),
    ("msgServiceFg", "Текст на этой плашке"),
    ("msgSelectOverlay", "Заливка поверх выделенного медиа"),
    ("msgWaveformInActive", "Прослушанная часть голосового, входящее"),
    ("msgWaveformOutActive", "Прослушанная часть голосового, исходящее"),
 ]),
 ("Поле ввода и низ чата", "Нижняя панель, иконки и кнопка вниз.", [
    ("historyComposeAreaBg", "Само поле ввода"),
    ("historyReplyBg", "Рамка вокруг поля, она же панель ответа и пересылки"),
    ("historyComposeAreaFg", "Текст, который печатаешь"),
    ("historyComposeIconFg", "Скрепка, смайлик, микрофон"),
    ("historyComposeIconFgOver", "Те же иконки под курсором"),
    ("historySendIconFg", "Стрелка отправки"),
    ("historyComposeButtonBg", "Панель Unmute, Join, Unblock"),
    ("historyComposeButtonBgOver", "Та же панель под курсором"),
    ("historyReplyIconFg", "Иконка слева в панели ответа"),
    ("historyReplyCancelFg", "Крестик отмены ответа"),
    ("historyToDownBg", "Круглая кнопка вниз"),
    ("historyToDownFg", "Стрелка в этой кнопке"),
    ("placeholderFg", "Подсказка в полях ввода"),
 ]),
 ("Аватарки без фото", "Градиент: первый цвет сверху, второй снизу.", [
    ("historyPeer1UserpicBg", "Аватарка 1, верх"), ("historyPeer1UserpicBg2", "Аватарка 1, низ"),
    ("historyPeer2UserpicBg", "Аватарка 2, верх"), ("historyPeer2UserpicBg2", "Аватарка 2, низ"),
    ("historyPeer3UserpicBg", "Аватарка 3, верх"), ("historyPeer3UserpicBg2", "Аватарка 3, низ"),
    ("historyPeer4UserpicBg", "Аватарка 4, верх"), ("historyPeer4UserpicBg2", "Аватарка 4, низ"),
    ("historyPeer5UserpicBg", "Аватарка 5, верх"), ("historyPeer5UserpicBg2", "Аватарка 5, низ"),
    ("historyPeer6UserpicBg", "Аватарка 6, верх"), ("historyPeer6UserpicBg2", "Аватарка 6, низ"),
    ("historyPeer7UserpicBg", "Аватарка 7, верх"), ("historyPeer7UserpicBg2", "Аватарка 7, низ"),
    ("historyPeer8UserpicBg", "Аватарка 8, верх"), ("historyPeer8UserpicBg2", "Аватарка 8, низ"),
    ("historyPeerSavedMessagesBg2", "Saved Messages, низ градиента"),
    ("historyPeerUserpicFg", "Буквы на аватарке"),
 ]),
 ("Имена участников в группах", "Восемь цветов, которыми подписаны отправители.", [
    ("historyPeer1NameFg", "Имя 1"), ("historyPeer2NameFg", "Имя 2"),
    ("historyPeer3NameFg", "Имя 3"), ("historyPeer4NameFg", "Имя 4"),
    ("historyPeer5NameFg", "Имя 5"), ("historyPeer6NameFg", "Имя 6"),
    ("historyPeer7NameFg", "Имя 7"), ("historyPeer8NameFg", "Имя 8"),
 ]),
 ("Меню, окна, кнопки", "Контекстные меню, диалоги, тосты.", [
    ("menuBg", "Фон контекстного меню"),
    ("menuBgOver", "Пункт меню под курсором"),
    ("menuIconFg", "Иконка пункта меню"),
    ("menuIconFgOver", "Иконка под курсором"),
    ("menuSeparatorFg", "Разделитель в меню"),
    ("boxBg", "Фон диалогового окна"),
    ("boxTitleFg", "Заголовок окна"),
    ("boxTextFg", "Текст в окне"),
    ("activeButtonBg", "Основная кнопка"),
    ("activeButtonFg", "Текст основной кнопки"),
    ("lightButtonFg", "Текстовая кнопка (Cancel, Save)"),
    ("attentionButtonFg", "Опасное действие (Delete, Log out)"),
    ("toastBg", "Фон всплывающего уведомления"),
    ("tooltipBg", "Фон подсказки"),
 ]),
 ("Звонки и медиа", "Плашка активного звонка, просмотрщик, плеер.", [
    ("callBarBg", "Плашка активного звонка"),
    ("callBarBgMuted", "Та же плашка с выключенным микрофоном"),
    ("callAnswerBg", "Кнопка ответа"),
    ("callHangupBg", "Кнопка сброса"),
    ("mediaviewBg", "Фон просмотрщика медиа"),
    ("mediaPlayerActiveFg", "Прослушанная часть в плеере"),
    ("mediaPlayerInactiveFg", "Оставшаяся часть в плеере"),
 ]),
]

data = []
for title, note, items in GROUPS:
    rows = []
    for key, label in items:
        if key not in raw:
            continue
        val = resolve(key)
        alpha = int(val[7:9], 16) / 255 if len(val) == 9 else 1.0
        rows.append({
            "key": key, "label": label, "value": val,
            "via": raw[key] if not raw[key].startswith("#") else "",
            "alpha": round(alpha * 100),
        })
    data.append({"title": title, "note": note, "rows": rows})

missing = [k for _, _, items in GROUPS for k, _ in items if k not in raw]
payload = json.dumps(data, ensure_ascii=False)

html = open(TEMPLATE, encoding="utf-8").read().replace("__DATA__", payload)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, "|", sum(len(g["rows"]) for g in data), "rows | missing:", missing or "none")
