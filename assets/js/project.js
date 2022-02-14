function readLanguageData(repo_url) {
    const repoURLComponents = repo_url.split("/");
    const repoName = repoURLComponents[repoURLComponents.length - 1];
    const url = `https://api.github.com/repos/cepdnaclk/${repoName}/languages`;

    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) {
            var total = 0;
            var count = 0;
            var langList = {};
            $.each(data, function(lang, usage) {
                total += usage;
                count += 1;
                langList[lang] = usage;
            });

            if (count > 0) {
                $(".langData").removeClass("d-none");

                $.each(langList, function(lang, usage) {
                    var p = usage / total;
                    var val = Math.round(p * 10000) / 100;

                    if (val >= 0.25) {
                        $("#langList").append(`<span class='tag m-2'>${lang} - ${val}%</span>`);
                    }
                });
            }
        }
    });
}

function readAPIData(url) {

    const apiBase = 'https://api.ce.pdn.ac.lk/projects/v1';
    const projData = url.split('/');

    const projBatch = projData[2].toUpperCase();
    const projCat = projData[1];

    const projTitle = url.replace(`/${projData[1]}/${projData[2]}/`, '');
    const apiURL = `${apiBase}/${projCat}/${projBatch}/${projTitle}/`;

    console.log(url, projCat, projBatch, projTitle);
    // console.log(projData);

    console.log('Fetch data from the API,', apiURL);
    $.ajax({
        type: "GET",
        url: apiURL,
        dataType: "json",
        success: function(data) {
            // Show remoteData container
            $(".remoteData").removeClass("d-none");

            // Team Data
            if (data.team && data.team[0] != "E/yy/xxx") {
                let teamCount = 0;

                $.each(data.team, function(index, member) {
                    if (index != "E/yy/xxx") {
                        let memberData = teamCard(member.name, index, member.profile_url, member.profile_image);

                        // console.log(memberData);
                        $("#teamCards").append(memberData);
                        teamCount++;
                    }
                });

                if(teamCount>0){
                    $(".remoteDataTeam_cards").removeClass("d-none");
                }
            }

            // Supervisor Data
            if (data.supervisors && data.supervisors[0] != "E/yy/xxx") {
                let supervisorsCount = Object.keys(data.supervisors).length;

                if(supervisorsCount>0){
                    $("#teamCards").append(divider());
                    $(".remoteDataTeam_cards").removeClass("d-none");
                }

                $.each(data.supervisors, function(index, member) {
                    if (index != "email@eng.pdn.ac.lk") {
                        let memberData = teamCard(member.name, "", member.profile_url, member.profile_image);

                        // console.log(memberData);
                        $("#teamCards").append(memberData);
                        supervisorsCount++;
                    }
                });
            }
        }
    });

}

function readRemoteData(basepath, page_url) {
    const url = `${page_url}/data/index.json`;

    console.log('Fetch data from the project config,', url);
    $.ajax({
        type: "GET",
        url: url,
        dataType: "json",
        success: function(data) {

            // Show remoteData container
            $(".remoteData").removeClass("d-none");

            // Tag Data
            if (data.tags.length > 0) {
                $(".remoteDataTags").removeClass("d-none");
                $.each(data.tags, function(index, tag) {
                    $("#tagList").append(`<a class="text-decoration-none text-dark" href="${basepath}/search/?query=${tag}"><span class='tag m-2'>${tag}</span></a> `);
                });
            }

            // Publication details
            if (data.publications != null && data.publications.length > 0) {
                let count = 0;

                $.each(data.publications, function(index, pub) {
                    // "title":"Paper Title",
                    // "journal":"Journal or Conference Name",
                    // "description":"Sample Description",
                    // "url":"#"

                    if (
                        pub.title !== "Paper Title" &&
                        pub.journal !== "Journal or Conference Name" &&
                        pub.description !== "Sample Description"
                    ) {
                        $("#publicationsURL").append("<li><div>");
                        $("#publicationsURL").append(
                            "<a href='" + pub.url + "' target='_blank'>" + pub.title + "</a>, " + pub.journal + "<br>"
                        );
                        $("#publicationsURL").append(
                            "<small>" + pub.description + "</small>"
                        );
                        $("#publicationsURL").append("</div></li>");
                    }
                });

                if (count > 0) {
                    $("#publications").removeClass("d-none");
                }
            }

            if (data.media != null && data.media.length > 0) {
                let count = 0;

                $.each(data.media, function(index, media) {
                    if (media.type === "youtube" && media.url.length > 0) {
                        if (!(media.title == "" || media.url =="#")) {
                            // Show the title

                            if(media.title != undefined ){
                                $("#youtubeVideoDiv").append("<h4>" + media.title + "</h4>");
                            }

                            $("#youtubeVideoDiv").append(
                                "<div class='video-container'><iframe width='100%' src='" +
                                media.url +
                                "' frameborder='1' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowfullscreen=''>"
                            );
                            $("#youtubeVideoDiv").append("</iframe></div>");
                            $("#youtubeVideoDiv").append("<br><br>");
                            count++;
                        }
                    } else {
                        // Only supported youtube videos for now
                    }
                });

                if (count > 0) {
                    $("#youtubeVideo").removeClass("d-none");
                }
            }

            // Removed, since it is already provided
            // $("#descriptionText").html(`<p>${data.description}</p>`);
        }
    });
}


function teamCard(name, eNumber, profile_url, avatar_url){
    let resp = `<div class="col-4 col-sm-3 col-md-2 col-lg-2 d-flex" style="padding: 3px;">
    <div class="card p-1 flex-fill">
    <div class="overflow-hidden">
    <img class="card-img-top img-fluid" src="${avatar_url}" alt="${name}">
    </div>
    <div class="card-body p-0 d-flex flex-column">
    <h4 class="profile-title card-title text-center pt-1">${name}</h4>
    <p class="profile-text card-text text-center">${eNumber}</p>`;

    if (profile_url != "#"){
        resp += `<div class="d-grid mt-auto px-2 pb-2">
        <a href="${profile_url}" target="_blank" class="btn btn-sm btn-primary btn-block">Profile</a>
        </div>`;
    }

    resp += `</div></div></div>`

    return resp;
}
function divider(){
    return `<div class="d-flex vr" style="width:24px; padding: 3px;"></div>`
}
