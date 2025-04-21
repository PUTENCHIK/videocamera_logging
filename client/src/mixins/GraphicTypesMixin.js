import { formatDate, firstToUpperCase } from '../utils/helpers';

import CamerasMixin from './CamerasMixin';
import ClassesMixin from './ClassesMixin';
import SnapshotsMixin from './SnapshotsMixin';

export default {
    mixins: [CamerasMixin, ClassesMixin, SnapshotsMixin],

    data() {
        return {
            source: null,
            chart_option: {},
            no_trackable_class_warning_shown: false,
            graphic_data: [],
            graphic_info: {},
        }
    },

    methods: {
        getClassById(id) {
            for (let i = 0; i < this.classes.length; i++) {
                let class_ = this.classes[i];
                if (class_.id === id) {
                    return class_;
                }
            };
        },

        getTitleText() {
            if (this.source == null) {
                return "Выберите категорию";
            } else {
                let result = "Статистика ";
                if (this.source.category == "camera") {
                    this.cameras.forEach((camera) => {
                        if (camera.id == this.source.id) {
                            result += `камеры #${camera.id}`;
                        }
                    });
                } else if (this.source.category == "class") {
                    this.classes.forEach((class_) => {
                        if (class_.id == this.source.id) {
                            result += `класса '${firstToUpperCase(class_.title)}'`;
                        }
                    });
                } else {
                    let cameras = [];
                    for (let i = 0; i < this.source.filters.cameras.length; i++) {
                        cameras.push(this.source.filters.cameras[i].id);
                    }
                    let classes = [];
                    for (let i = 0; i < this.source.filters.classes.length; i++) {
                        classes.push(this.source.filters.classes[i].name);
                    }
                    result = `Классы (${classes.join(", ")}) на камерах ${cameras.join(", ")}`;
                }
                return result;
            }
        },

        getGrid() {
            return {
                left: 40,
                right: 40,
                bottom: 40,
                top: 80
            }
        },

        getTooltip() {
            return {
                trigger: 'item',
                formatter: (item) => {
                    let object = item.value[2];
                    let title = object.trackable_class ?
                        object.trackable_class.title : "неизвестный класс";
                    return `
                        <b>${firstToUpperCase(title)}</b><br>
                        Добавлен: ${formatDate(object.created_at)}<br>
                        Метка: ${object.label}<br>
                        Вероятность: ${object.probability}<br>
                        ID камеры: ${object.snapshot.camera_id}<br>
                        ID снимка: ${object.snapshot_id}
                    `;
                }
            };
        },

        getToolbox() {
            return {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                }
            };
        },

        getDatazoom() {
            return [
                {
                    type: 'inside',
                    start: 0,
                    end: 100
                },
                {
                    start: 0,
                    end: 100
                }
            ]
        },

        getTrackableClassName(object) {
            if (object.trackable_class) {
                return object.trackable_class.name;
            } else {
                if (!this.no_trackable_class_warning_shown) {
                    this.addWarning("Неизвестный класс",
                        `В базе хранятся объекты с меткой ${object.label}, для которой не задан класс`);
                    this.no_trackable_class_warning_shown = true;
                }
                return "unknown";
            }
        },

        getObjectData(object) {
            let date = new Date(object.created_at);
            let image_name = this.getTrackableClassName(object);
            return {
                value: [date, object.probability, object],
                symbol: `image:///src/assets/icons/${image_name}.png`,
                symbolSize: 32,
                symbolOffset: [0, 0],
            };
        },

        getCamerasData() {
            let data = [];
            this.objects.forEach((object) => {
                if (object.snapshot.camera_id == this.source.id) {
                    data.push(this.getObjectData(object));
                }
            });
            return data;
        },

        getClassesData() {
            let data = [];
            this.objects.forEach((object) => {
                let tc = object.trackable_class;
                if (tc && tc.id == this.source.id) {
                    data.push(this.getObjectData(object));
                }
            });
            return data;
        },

        getMixedData() {
            let cameras_ids = [];
            let classes_ids = [];
            this.source.filters.cameras.forEach((camera_item) => {
                cameras_ids.push(camera_item.id);
            });
            this.source.filters.classes.forEach((class_item) => {
                classes_ids.push(class_item.id);
            });
            let data = [];

            this.objects.forEach((object) => {
                let cam_id = object.snapshot.camera_id;
                let tc = object.trackable_class;
                if (!this.source.filters.classes.length && cameras_ids.includes(cam_id)) {
                    data.push(this.getObjectData(object));
                } else if (!this.source.filters.cameras.length && tc && classes_ids.includes(tc.id)) {
                    data.push(this.getObjectData(object));
                } else {
                    if (cameras_ids.includes(cam_id) && tc && classes_ids.includes(tc.id)) {
                        data.push(this.getObjectData(object));
                    }
                }
            });

            return data;
        },

        getData() {
            let data = [];
            if (this.source.category == "camera") {
                data = this.getCamerasData();
                if (!data.length) {
                    this.addWarning("Нет объектов",
                        `Для камеры #${this.source.id} не было сохранено ни одного объекта`
                    );
                }
            } else if (this.source.category == "class") {
                data = this.getClassesData();
                if (!data.length) {
                    let class_ = this.getClassById(this.source.id);
                    this.addWarning("Нет объектов",
                        `В базе нет ни одного объекта класса '${firstToUpperCase(class_.title)}'`
                    );
                }
            } else {
                data = this.getMixedData();
                if (!data.length) {
                    this.addWarning("Нет объектов",
                        `По результатам выборки не было найдено ни одного объекта`
                    );
                }
            }
            
            return data;
        },

        updateChartOption() {
            this.graphic_data = this.getData();
            this.updateGraphicInfo();
            this.chart_option = {
                title: {
                    text: this.getTitleText(),
                    top: 20,
                    left: 'center',
                },
                grid: this.getGrid(),
                tooltip: this.getTooltip(),
                toolbox: this.getToolbox(),
                dataZoom: this.getDatazoom(),
                xAxis: {
                    type: 'time',
                    boundaryGap: false
                },
                yAxis: {
                    type: 'value',
                },
                series: [
                    {
                        data: this.graphic_data,
                        type: 'scatter',
                    }
                ]
            };
        },

        updateGraphicInfo() {
            this.graphic_info.amount = this.graphic_data.length;
            if (this.graphic_info.amount) {
                let min_date = this.graphic_data[0].value[2].created_at;
                let max_date = this.graphic_data[0].value[2].created_at;
                if (this.graphic_info.amount > 1) {
                    for (let i = 1; i < this.graphic_data.length; i++) {
                        let date = this.graphic_data[i].value[2].created_at;
                        min_date = date < min_date ? date : min_date;
                        max_date = date > max_date ? date : max_date;
                    }
                }
                this.graphic_info.min_date = min_date;
                this.graphic_info.max_date = max_date;
                console.log(min_date, max_date);
                
            }
        }
    },

    async mounted() {
        await this.loadCameras();
        await this.loadClasses();
        await this.loadSnapshots();
        await this.loadObjects();
    }
}