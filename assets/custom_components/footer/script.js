
// let div = document.createElement('div');
// div.innerHTML = '<p>This is an document.createElement example</p>';
// document.body.appendChild(div);

let linkFaIcons = document.createElement('link');
linkFaIcons.rel = "stylesheet"
linkFaIcons.href = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css";
document.head.appendChild(linkFaIcons)

// let footerMainSection = document.createElement("div");
// footerMainSection.innerHTML = footerMainSection.innerHTML + '<h1 style="position: fixed;">WHAT IS THIS</h1>';
// // let appViewContainer = document.getElementsByClassName('appview-container')
// // appViewContainer.append()
// // appViewContainer.appendChild("")
// document.body.appendChild(footerMainSection);

const injectCSS = css => {
    let el = document.createElement('style');
    el.type = 'text/css';
    el.innerText = css;
    document.head.appendChild(el);
    return el;
};

injectCSS("__CUSTOM_CSS__");