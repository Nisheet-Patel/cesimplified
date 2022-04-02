select_course(document.getElementById("all-topic"), '0');

var pre;
function select_course(course,id){
    if(pre){
        pre.style.color = '#968AB6';
    }
    course.style.color = '#3B3086';
    pre = course;

    fetch('/get/course/'+id)
        .then(function (response) {
            return response.json();
        }).then(function (data) {
            if(document.getElementById("course-container") != null){
                var div = document.getElementById('course-container');
                div.innerHTML = "";
                for(a in data.topic){
                    topic = data.topic[a]
                    console.log(topic.img_name)
                    div.innerHTML += `
                    <section>
                        <a href="/course/${topic.course_title}/${topic.id}">
                        <div class="course-img" style="content: url('static/images/${topic.img_name}');"></div>
                        <div class="course-details">
                            <div class="course-title">
                                ${topic.title}
                            </div>
                            <div class="course-metadata">
                                Videos: ${topic.total_videos}  |  ${topic.course_title}
                            </div>
                        </div>
                        </a>
                    </section>
                    `
                }
            }
        });
};