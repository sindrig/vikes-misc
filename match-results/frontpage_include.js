if(window.location.pathname === "/") {
    var ifrm = document.createElement("iframe");
    ifrm.setAttribute("src", "http://vikes-result.irdn.is/");
    ifrm.style.height = "480px";
    var container = document.getElementById("s5_pos_custom_1");
    if (window.getScrollWidth && window.getScrollWidth() < 500){
        ifrm.style.width = "100%";
        container.parentNode.insertBefore(ifrm, container.nextSibling);
    } else {
        ifrm.style.position = "absolute";
        ifrm.style.right = "100px";
        ifrm.style.top = "20px";
        ifrm.style.width = "400px";
        ifrm.style.maxWidth = "60%";
        container.appendChild(ifrm);
    }
}else if(window.location.pathname === "/leikir-vikings") {
    var ifrm = document.createElement("iframe");
    ifrm.style.width = "100%";
    ifrm.style.minHeight = "1600px";
    ifrm.setAttribute("src", "http://vikes-result.irdn.is/matchpage.html");
    var elements = document.getElementsByClassName('item-page');
    elements[0].appendChild(ifrm);
    document.getElementById('s5_component_wrap_inner').style.padding = '0';
}
