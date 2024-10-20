const path = window.location.pathname.split("/");
const changeIndex = path.indexOf("change");
const isEdit = changeIndex !== -1;
const productId = path[changeIndex - 1];

let productImgGroup;
let uploadedImgs;

const handleImgsChange = (e) => {
  const nodesToRemove = productImgGroup.querySelectorAll(
    ".product-img-new-uploading"
  );
  for (let node of nodesToRemove) {
    node.remove();
  }

  addButton = productImgGroup.querySelector(".add-row").querySelector("a");
  console.dir(e.target);
  const files = e.target.files;

  for (let file of files) {
    addButton.dispatchEvent(new Event("click", { bubbles: true }));
    const imgs = productImgGroup.querySelectorAll(".dynamic-img_urls");
    const lastImg = imgs[imgs.length - 1];
    lastImg.classList.add("product-img-new-uploading");

    const input = lastImg.querySelector(".field-img_url").firstElementChild;

    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    input.files = dataTransfer.files;
    input.addEventListener("change", handleOneImgChange);

    const img = document.createElement("img");
    img.width = 150;
    img.height = 150;
    img.style = "display: block; object-fit: contain";
    input.after(img);

    input.dispatchEvent(new Event("change", { bubbles: true }));
  }
};

const deleteOneNewImg = (e) => {
  if (e.target.className === "inline-deletelink") {
    e.preventDefault();
    e.currentTarget.remove();
  }
};

const handleOneImgChange = (e) => {
  const input = e.target;
  let parent = input.parentElement;
  if (parent.tagName !== "TD") {
    parent = parent.parentElement;
  }
  const img = parent.querySelector("img");
  img.src = URL.createObjectURL(input.files[0]);
};

const handleLoad = () => {
  productImgGroup = document.getElementById("img_urls-group");
  uploadedImgs = productImgGroup.querySelectorAll(".dynamic-img_urls");
  for (let img of uploadedImgs) {
    if (!img.classList.contains("has_original")) {
      img.remove();
      continue;
    }
    const input = img.querySelector(".field-img_url input");
    input.addEventListener("change", handleOneImgChange);
  }

  const multiUpload = document.querySelector("#mulitple_product_img_upload");
  multiUpload.addEventListener("change", handleImgsChange);
};

window.addEventListener("load", handleLoad);
