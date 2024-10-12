import Alpine from 'alpinejs';
import mask from '@alpinejs/mask';
import persist from "@alpinejs/persist";
import hljs from 'highlight.js';
import javascript from 'highlight.js/lib/languages/javascript';
import 'highlight.js/styles/devibeans.css';
import 'htmx.org';
import htmx from 'htmx.org'
import _hyperscript from 'hyperscript.org';
import Sortable from 'sortablejs';
import { Carousel, initTWE, Input, Modal, Ripple } from 'tw-elements';
// import { Carousel, initTWE, Input, Modal, Ripple, Collapse, } from 'tw-elements';
// import { Carousel, initTWE } from "tw-elements";
// const htmx = require('htmx.org');
window.Alpine = Alpine;
window.htmx = htmx;

// (window as any).htmx.config.defaultSwapStyle = 'outerHTML';
// (window as any).htmx.config.historyEnabled = true;
// (window as any).htmx.config.historyCacheSize = 10;
// (window as any).htmx.config.refreshOnHistoryMiss = true;
// (window as any).htmx.config.useTemplateFragments = true;

htmx.config.defaultSwapStyle = 'outerHTML';
htmx.config.historyEnabled = true;
htmx.config.historyCacheSize = 10;
htmx.config.refreshOnHistoryMiss = true;
htmx.config.useTemplateFragments = true;

htmx.onLoad(function (content: { querySelectorAll: (arg0: string) => NodeListOf<Element> }) {
    const sortables = content.querySelectorAll('.sortable');
    for (let i = 0; i < sortables.length; i++) {
        const sortable = sortables[i];
        new Sortable(sortable as HTMLElement, {
            animation: 150,
            ghostClass: 'blue-background-class',
        });
    }
});
Alpine.plugin(mask)
Alpine.plugin(persist)
Alpine.start();
_hyperscript.browserInit();

hljs.highlightAll();
hljs.registerLanguage('javascript', javascript);

initTWE({ Modal, Ripple, Carousel, Input }, { allowReinits: true });
// initTWE({ Modal, Ripple, Carousel, Input, Collapse }, { allowReinits: true });


import './backtotop';
