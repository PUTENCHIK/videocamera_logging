const Message = {
    props: {
        type: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        text: {
            type: String,
            required: true,
        },
    },
    template: `
        <div class="message" :class="type">
            <div class="icon-wrapper">
                <div class="img"></div>
            </div>
            <div class="__content">
                <div class="title label-bold">{{ title }}</div>
                <div class="text">{{ text }}</div>
            </div>
        </div>
    `
};

export default Message;