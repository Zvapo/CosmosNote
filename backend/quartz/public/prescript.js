(function(){var r=window.matchMedia("(prefers-color-scheme: light)").matches?"light":"dark",h=localStorage.getItem("theme")??r;document.documentElement.setAttribute("saved-theme",h);var m=n=>{let d=new CustomEvent("themechange",{detail:{theme:n}});document.dispatchEvent(d)};document.addEventListener("nav",()=>{let n=t=>{let e=document.documentElement.getAttribute("saved-theme")==="dark"?"light":"dark";document.documentElement.setAttribute("saved-theme",e),localStorage.setItem("theme",e),m(e)},d=t=>{let e=t.matches?"dark":"light";document.documentElement.setAttribute("saved-theme",e),localStorage.setItem("theme",e),m(e)},a=document.querySelector("#darkmode");a&&(a.addEventListener("click",n),window.addCleanup(()=>a.removeEventListener("click",n)));let c=window.matchMedia("(prefers-color-scheme: dark)");c.addEventListener("change",d);let o=t=>{if(t.data?.type==="changeTheme"){let e=t.data.theme;document.documentElement.setAttribute("saved-theme",e),localStorage.setItem("theme",e),m(e)}};window.addEventListener("changeTheme",o),window.addCleanup(()=>{window.removeEventListener("changeTheme",o),c.removeEventListener("change",d)})})})();
