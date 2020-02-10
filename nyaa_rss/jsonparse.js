function create(content, i) {
  var linebreak = document.createElement("br");
  var p_title = document.createElement("p");
  var t_title = document.createTextNode(content.title);
  p_title.appendChild(t_title);

  var d_details = document.createElement("div");
  d_details.setAttribute('id', `Details ${i}`);
  d_details.setAttribute('class', 'detail');

  var p_link = document.createElement("a");
  var t_link = document.createTextNode("Link to Torrent");
  p_link.appendChild(t_link);
  p_link.setAttribute('href', content.details.t_link);

  var p_slink = document.createElement("a");
  var t_slink = document.createTextNode("Link to Nyaa");
  p_slink.appendChild(t_slink);
  p_slink.setAttribute('href', content.details.link);

  var p_size = document.createElement("p");
  var t_size = document.createTextNode(content.details.size);
  p_size.appendChild(t_size);

  var p_IsTrusted = document.createElement("p");
  var t_IsTrusted = document.createTextNode(` Trusted : ${content.details.IsTrusted}`);
  p_IsTrusted.appendChild(t_IsTrusted);

  d_details.appendChild(p_link);
  d_details.appendChild(linebreak);
  d_details.appendChild(p_slink);
  d_details.appendChild(p_size);
  d_details.appendChild(p_IsTrusted);

  var my_div = document.createElement("div");
  my_div.setAttribute('id', `Entries ${i}`);
  my_div.setAttribute('class', 'entry');
  my_div.appendChild(p_title);
  my_div.appendChild(d_details);
  var element = document.getElementById("div1");
  element.appendChild(my_div);
};
function myparse() {
  var xmlhttp = new XMLHttpRequest();
  xmlhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var myObj = JSON.parse(this.responseText);
      const entries = Object.entries(myObj);
      for (const [num, entry] of entries) {
        create(entry, num);
        console.log(entry.details)
      }
    }
  };
  xmlhttp.open("GET", "data.json", true);
  xmlhttp.send();
}
